from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from app.models.material import Material, AISummary
from app import db
import openai
from config import Config
import os

ai = Blueprint('ai', __name__)

# Initialize OpenAI client
openai.api_key = Config.OPENAI_API_KEY

@ai.route('/ai')
@login_required
def index():
    return render_template('ai.html')

@ai.route('/ai/summarize', methods=['POST'])
@login_required
def summarize_material():
    material_id = request.form.get('material_id')
    
    material = Material.query.get_or_404(material_id)
    
    # Check if user has access to this material
    # (Either they own it or they're in the group it belongs to)
    
    # Read the file content (simplified - would need to handle different file types)
    file_path = os.path.join(Config.UPLOAD_FOLDER, material.file_path)
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Truncate content if it's too long
    if len(content) > 4000:
        content = content[:4000]
    
    # Call OpenAI API to summarize
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes educational content."},
                {"role": "user", "content": f"Please summarize the following educational material: {content}"}
            ]
        )
        
        summary = response.choices[0].message.content
        
        # Save the summary
        ai_summary = AISummary(material_id=material.id, summary_text=summary)
        db.session.add(ai_summary)
        db.session.commit()
        
        return jsonify({"success": True, "summary": summary})
    
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@ai.route('/ai/ask', methods=['POST'])
@login_required
def ask_question():
    question = request.form.get('question')
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful educational assistant."},
                {"role": "user", "content": question}
            ]
        )
        
        answer = response.choices[0].message.content
        
        return jsonify({"success": True, "answer": answer})
    
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})
