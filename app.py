from flask import Flask, render_template, request, jsonify
from media_generator import MediaGenerator
from main import AIAssistant
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

# Initialize generators
media_gen = MediaGenerator()
ai_assistant = AIAssistant()

@app.route('/')
def index():
    """Render the main dashboard"""
    return render_template('index.html')

# ==================== MEDIA GENERATOR ROUTES ====================

@app.route('/api/media/image', methods=['POST'])
def generate_images():
    """Generate images from query"""
    try:
        data = request.get_json()
        query = data.get('query', '')
        source = data.get('source', 'unsplash')
        count = int(data.get('count', 1))
        
        if not query:
            return jsonify({'error': 'Query is required'}), 400
        
        images = media_gen.generate_image(query, source, count)
        return jsonify({
            'success': True,
            'type': 'image',
            'count': len(images),
            'media': images
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/media/video', methods=['POST'])
def generate_videos():
    """Generate videos from query"""
    try:
        data = request.get_json()
        query = data.get('query', '')
        source = data.get('source', 'pexels')
        count = int(data.get('count', 1))
        
        if not query:
            return jsonify({'error': 'Query is required'}), 400
        
        videos = media_gen.generate_video(query, source, count)
        return jsonify({
            'success': True,
            'type': 'video',
            'count': len(videos),
            'media': videos
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/media/music', methods=['POST'])
def generate_music():
    """Generate music from query"""
    try:
        data = request.get_json()
        query = data.get('query', '')
        source = data.get('source', 'freesound')
        count = int(data.get('count', 1))
        
        if not query:
            return jsonify({'error': 'Query is required'}), 400
        
        tracks = media_gen.generate_music(query, source, count)
        return jsonify({
            'success': True,
            'type': 'music',
            'count': len(tracks),
            'media': tracks
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/media/history', methods=['GET'])
def get_media_history():
    """Get media generation history"""
    try:
        history = media_gen.get_media_history()
        stats = media_gen.get_stats()
        return jsonify({
            'success': True,
            'history': history,
            'stats': stats
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/media/clear', methods=['POST'])
def clear_media_history():
    """Clear media history"""
    try:
        media_gen.clear_history()
        return jsonify({'success': True, 'message': 'History cleared'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ==================== AI ASSISTANT ROUTES ====================

@app.route('/api/ai/chat', methods=['POST'])
def ai_chat():
    """Send message to AI assistant"""
    try:
        data = request.get_json()
        message = data.get('message', '')
        
        if not message:
            return jsonify({'error': 'Message is required'}), 400
        
        response = ai_assistant.chat(message)
        return jsonify({
            'success': True,
            'message': message,
            'response': response
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/ai/history', methods=['GET'])
def get_ai_history():
    """Get AI conversation history"""
    try:
        history = ai_assistant.get_history()
        return jsonify({
            'success': True,
            'history': history
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/ai/clear', methods=['POST'])
def clear_ai_history():
    """Clear AI conversation history"""
    try:
        ai_assistant.clear_history()
        return jsonify({'success': True, 'message': 'Conversation cleared'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
