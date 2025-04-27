from flask import Blueprint, jsonify, request
from ..models.user import User
from ..models.database import Database
from ..services.resume_parser import ResumeParserService
from ..services.pdf_service import save_uploaded_file

user_bp = Blueprint('user', __name__)

class UserController:
    def __init__(self):
        self.db = Database()
        self.resume_parser = ResumeParserService()

    def register_user(self):
        data = request.get_json()
        user = User(name=data['name'], email=data['email'], password=data['password'])
        user.save()
        return jsonify({"message": "User registered successfully!"}), 201

    def upload_resume(self):
        if 'resume' not in request.files:
            return jsonify({"error": "No file part"}), 400
        file = request.files['resume']
        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400
        file_path = save_uploaded_file(file)
        resume_data = self.resume_parser.parse_resume(file_path)
        return jsonify(resume_data), 200

    def get_user_profile(self, user_id):
        user = User.query.get(user_id)
        if user:
            return jsonify({
                'id': user.id,
                'username': user.username,
                'email': user.email
            }), 200
        return jsonify({'error': 'User not found'}), 404

@user_bp.route('/<int:user_id>', methods=['GET'])
def get_profile(user_id):
    controller = UserController()
    return controller.get_user_profile(user_id)