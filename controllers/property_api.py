import json
from odoo import http
from odoo.http import request


class PropertyApi(http.Controller):

    @http.route("/v1/property", methods=["POST"], type="http", auth="none", csrf=False)
    def post_property(self):
        args = request.httprequest.data.decode()
        vals = json.loads(args)
        if not vals.get('name'):
            return request.make_json_response({
                'message': "name is required",
            }, status=400)
        try:
            sequence = request.env['ir.sequence'].next_by_code('property_sequence')
            vals['ref'] = sequence
            res = request.env['property'].sudo().create(vals)
            if res:
                return request.make_json_response({
                    "message": "property has been created",
                    "name": res.name,
                }, status=201)
        except Exception as error:
            return request.make_json_response({
                'message': error,
            }, status=400)



    @http.route("/v1/property/<int:property_id>", methods=["PUT"], type="http", auth="none", csrf=False)
    def update_property(self, property_id):
        try:
            property_id = request.env['property'].sudo().search([('id', '=', property_id)])
            if not property_id:
                return request.make_json_response({
                    'message': 'Record not found!'
                }, status=400)

            args = request.httprequest.data.decode()
            vals = json.loads(args)
            property_id.write(vals)
            return request.make_json_response({
                "message": "property has been updated",
                "id": property_id.id,
                "name": property_id.name,
            }, status=200)

        except Exception as error:
            return request.make_json_response({
                'message': error,
            }, status=400)

    @http.route("/v1/property/<int:property_id>", methods=["GET"], type='http', auth='none', csrf=False)
    def get_property(self, property_id):
        try:
            property_id = request.env['property'].sudo().search([('id', '=', property_id)])
            if not property_id:
                return request.make_json_response({
                    'message': 'Record not found!'
                }, status=400)

            args = request.httprequest.data.decode()
            vals = json.loads(args)
            property_id.write(vals)
            return request.make_json_response({
                "id": property_id.id,
                "ref": property_id.ref,
                "name": property_id.name,
                "post_code": property_id.post_code,
                "bedrooms": property_id.bedrooms,
            }, status=200)
        except Exception as error:
            return request.make_json_response({
                'message': error,
            }, status=400)

