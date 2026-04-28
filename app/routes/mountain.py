from flask import Blueprint, render_template, request, redirect, url_for, flash
# from app.models.mountain import Mountain
# from app.models.user_comment import UserComment

mountain_bp = Blueprint('mountain', __name__, url_prefix='/mountain')

@mountain_bp.route('/<int:mountain_id>')
def detail(mountain_id):
    """
    山岳詳細資訊頁面：顯示單筆山岳資料與留言。
    - 呼叫 Mountain.get_by_id(mountain_id)
    - 呼叫 UserComment.get_by_mountain_id(mountain_id)
    - 渲染 templates/detail.html
    - 若無資料則回傳 404
    """
    pass

@mountain_bp.route('/<int:mountain_id>/comment', methods=['POST'])
def add_comment(mountain_id):
    """
    新增評論：接收表單並存入資料庫。
    - 取得表單 request.form 的 user_name 與 comment_content
    - 驗證資料是否為空
    - 呼叫 UserComment.create()
    - 成功後重導向回 /mountain/<mountain_id>
    """
    pass
