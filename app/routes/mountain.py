from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.mountain import Mountain
from app.models.user_comment import UserComment

mountain_bp = Blueprint('mountain', __name__, url_prefix='/mountain')

@mountain_bp.route('/<int:mountain_id>')
def detail(mountain_id):
    """山岳詳細資訊頁面：顯示單筆山岳資料與留言"""
    mountain = Mountain.get_by_id(mountain_id)
    
    if not mountain:
        return render_template('404.html'), 404
        
    comments = UserComment.get_by_mountain_id(mountain_id)
    return render_template('detail.html', mountain=mountain, comments=comments)

@mountain_bp.route('/<int:mountain_id>/comment', methods=['POST'])
def add_comment(mountain_id):
    """新增評論：接收表單並存入資料庫"""
    # 檢查山岳是否存在
    mountain = Mountain.get_by_id(mountain_id)
    if not mountain:
        return render_template('404.html'), 404

    user_name = request.form.get('user_name', '').strip()
    comment_content = request.form.get('comment_content', '').strip()
    
    # 基礎驗證
    if not user_name or not comment_content:
        flash('姓名與評論內容為必填欄位', 'danger')
        return redirect(url_for('mountain.detail', mountain_id=mountain_id))
        
    # 儲存到資料庫
    data = {
        'mountain_id': mountain_id,
        'user_name': user_name,
        'comment_content': comment_content
    }
    
    comment_id = UserComment.create(data)
    
    if comment_id:
        flash('評論已成功發布！', 'success')
    else:
        flash('評論發布失敗，請稍後再試', 'danger')
        
    return redirect(url_for('mountain.detail', mountain_id=mountain_id))
