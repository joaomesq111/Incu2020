from flask import render_template
from app import app


@app.errorhandler(404)
def not_found_error(error):
    return render_template('error_templates/code_errors/404.html', error=error), 404


@app.errorhandler(500)
def internal_error(error):
    return render_template('error_templates/code_errors/500.html', error=error), 500
