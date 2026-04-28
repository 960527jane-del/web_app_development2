from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.mountain import Mountain

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """首頁：顯示所有山岳列表"""
    mountains = Mountain.get_all()
    return render_template('index.html', mountains=mountains)

@main_bp.route('/search')
def search():
    """搜尋山岳：接收 Query String 並過濾山岳列表"""
    keyword = request.args.get('q', '').strip()
    
    if keyword:
        mountains = Mountain.search(keyword)
        if not mountains:
            flash(f'找不到與「{keyword}」相關的山岳', 'warning')
    else:
        mountains = Mountain.get_all()
        
    return render_template('index.html', mountains=mountains, keyword=keyword)
