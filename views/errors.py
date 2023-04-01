from flask import Blueprint, render_template, make_response

errors = Blueprint('errors', __name__)

@errors.app_errorhandler(404)
def page_not_found(e):
    error = {
        'code':404,
        'title':'Oops! Page not found',
        'message':"Your page don't exist.."
    }
    response = make_response(render_template('error.html', error=error))
    response.status_code = 404
    return response

@errors.app_errorhandler(401)
def unauthorized(e):
    error = {
        'code':401,
        'title':'Oops! Unauthorized',
        'message':"You are not authorized to access this resource."
    }
    response = make_response(render_template('error.html', error=error))
    response.status_code = 401
    return response

@errors.app_errorhandler(403)
def forbidden(e):
    error = {
        'code':403,
        'title':'Oops! Forbidden',
        'message':"You don't have permission to access this resource."
    }
    response = make_response(render_template('error.html', error=error))
    response.status_code = 403
    return response

@errors.app_errorhandler(500)
def internal_server_error(e):
    error = {
        'code':500,
        'title':'Oops! Internal Server Error',
        'message':"An error occurred while processing your request."
    }
    response = make_response(render_template('error.html', error=error))
    response.status_code = 500
    return response
