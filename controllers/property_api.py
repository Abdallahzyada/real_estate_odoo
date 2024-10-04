import json
import math

from odoo import http
from odoo.http import request
from urllib.parse import parse_qs

def valid_response(data, pagination_info, status):
    response_body = {
        "data": data,
    }
    if pagination_info:
        response_body['pagination_info'] = pagination_info
    return request.make_json_response(response_body, status=status)

def invalid_response(error, status):
    response_body = {
        "error": error
    }
    return request.make_json_response(response_body, status=status)

class PropertyApi(http.Controller):

    @http.route("/v1/property", methods=["POST"], type="http", auth="none", csrf=False)
    def post_property(self):
        args = request.httprequest.data.decode()
        vals = json.loads(args)
        if not vals.get('name'):
            return invalid_response("name is required", 400)
        try:
            sequence = request.env['ir.sequence'].next_by_code('property_sequence')
            vals['ref'] = sequence
            res = request.env['property'].sudo().create(vals)
            if res:
                return valid_response({
                    "message": "property has been created",
                    "name": res.name,
                }, 201)
        except Exception as error:
            return invalid_response(error, 400)



    @http.route("/v1/property/<int:property_id>", methods=["PUT"], type="http", auth="none", csrf=False)
    def update_property(self, property_id):
        try:
            property_id = request.env['property'].sudo().search([('id', '=', property_id)])
            if not property_id:
                return invalid_response('Record not found!', 400)

            args = request.httprequest.data.decode()
            vals = json.loads(args)
            property_id.write(vals)
            return valid_response({
                "message": "property has been updated",
                "id": property_id.id,
                "name": property_id.name,
            }, 200)

        except Exception as error:
            return invalid_response(error, 400)

    @http.route("/v1/property/<int:property_id>", methods=["GET"], type='http', auth='none', csrf=False)
    def get_property(self, property_id):
        try:
            property_id = request.env['property'].sudo().search([('id', '=', property_id)])
            if not property_id:
                return invalid_response('Record not found!',400)

            args = request.httprequest.data.decode()
            vals = json.loads(args)
            property_id.write(vals)
            return valid_response({
                "id": property_id.id,
                "ref": property_id.ref,
                "name": property_id.name,
                "post_code": property_id.post_code,
                "bedrooms": property_id.bedrooms,
            }, 200)

        except Exception as error:
            return invalid_response(error, 400)


    @http.route("/v1/property/<int:property_id>", methods=["DELETE"], type='http', auth='none', csrf=False)
    def delete_property(self, property_id):
        try:
            property_id = request.env['property'].sudo().search([('id', '=', property_id)])
            if not property_id:
                return invalid_response('Record not found!', 400)

            args = request.httprequest.data.decode()
            vals = json.loads(args)
            property_id.unlink()
            return valid_response({
                "message": "record deleted"
            }, 200)

        except Exception as error:
            return invalid_response(error, 400)


    @http.route("/v1/properties", methods=["GET"], type='http', auth='none', csrf=False)
    def get_property_list(self):
        try:
            params = parse_qs(request.httprequest.query_string.decode('utf-8'))
            property_domain = []
            page=offset=None
            limit = 5
            if params:
                if params.get("limit"):
                    limit = int(params.get("limit")[0])
                if params.get("page"):
                    page = int(params.get("page")[0])

            if page:
                offset = (page * limit) - limit
            if params.get('state'):
                property_domain += [('state', '=', params.get('state')[0])]
            property_ids = request.env['property'].sudo().search(property_domain, offset=offset, limit=limit, order='id desc')
            property_count = request.env['property'].sudo().search_count(property_domain)
            if not property_ids:
                return invalid_response("No record found", 400)

            return valid_response([{
                "id": property.id,
                "ref": property.ref,
                "name": property.name,
                "post_code": property.post_code,
                "bedrooms": property.bedrooms,
            } for property in property_ids], pagination_info={
                "page": page if page else 1,
                "limit": limit,
                "pages": math.ceil(property_count / limit) if limit else 1,
                "count": property_count,
            },status=200)

        except Exception as error:
            return invalid_response(error, 400)