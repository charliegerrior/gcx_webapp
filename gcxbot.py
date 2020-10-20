from app import app, db
from app.models import Submission, Offer

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Submission': Submission, 'Offer': Offer}