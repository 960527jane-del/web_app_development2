from flask import Blueprint, render_template, request, redirect, url_for, flash
# from app.models.mountain import Mountain

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """
    首頁：顯示搜尋框與所有山岳列表。
    - 呼叫 Mountain.get_all()
    - 渲染 templates/index.html
    """
    pass

@main_bp.route('/search')
def search():
    """
    搜尋山岳：接收 Query String 並過濾山岳列表。
    - 取得 request.args.get('q')
    - 呼叫 Mountain.search(keyword)
    - 渲染 templates/index.html，傳入結果
    """
    pass
