from flask import render_template
from app import app
from pymongo import errors


@app.errorhandler(errors.OperationFailure)
def internal_operation_error(error):
    return render_template('error_templates/code_errors/500.html', error=error), 500


@app.errorhandler(errors.WriteError)
def internal_write_error(error):
    return render_template('error_templates/code_errors/500.html', error=error), 500


@app.errorhandler(404)
def not_found_error(error):
    return render_template('error_templates/code_errors/404.html', error=error), 404
