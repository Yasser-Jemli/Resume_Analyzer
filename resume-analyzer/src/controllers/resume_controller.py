from flask import Blueprint, request, jsonify
from ..models.resume import Resume
from ..models.database import Database

resume_bp = Blueprint('resume', __name__)

class ResumeController:
    def __init__(self):
        self.db = Database()

    def upload_resume(self):
        if 'resume' not in request.files:
            return jsonify({"error": "No file part"}), 400
        
        file = request.files['resume']
        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400
        
        if file:
            try:
                from ..services.pdf_service import save_uploaded_file
                from ..services.resume_parser import parse_resume
                
                file_path = save_uploaded_file(file)
                resume_data = parse_resume(file_path)
                
                if resume_data:
                    self.db.insert_resume(resume_data)
                    return jsonify({"message": "Resume uploaded and analyzed successfully", "data": resume_data}), 200
                else:
                    return jsonify({"error": "Failed to parse resume"}), 500
            except ImportError as e:
                return jsonify({"error": f"Service not available: {str(e)}"}), 500
            except Exception as e:
                return jsonify({"error": f"Error processing resume: {str(e)}"}), 500

    def get_resume_analysis(self, resume_id):
        resume = self.db.get_resume(resume_id)
        if resume:
            return jsonify(resume), 200
        return jsonify({"error": "Resume not found"}), 404

@resume_bp.route('/upload', methods=['POST'])
def upload():
    controller = ResumeController()
    return controller.upload_resume()

@resume_bp.route('/<int:resume_id>', methods=['GET'])
def get_analysis(resume_id):
    controller = ResumeController()
    return controller.get_resume_analysis(resume_id)