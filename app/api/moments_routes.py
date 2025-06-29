"""
朋友圈相关API路由
实现朋友圈功能 (Plus版)
"""

from flask import Blueprint, jsonify, request
from app.auth import require_api_key
from app.unified_logger import logger
from app.wechat import wechat_manager

moments_bp = Blueprint('moments', __name__)

@moments_bp.route('/open', methods=['POST'])
@require_api_key
def open_moments():
    """进入朋友圈 (Plus版)"""
    wx_instance = wechat_manager.get_instance()
    if not wx_instance:
        return jsonify({
            'code': 2001,
            'message': '微信未初始化',
            'data': None
        }), 400

    try:
        # 检查当前使用的库
        lib_name = getattr(wx_instance, '_lib_name', 'wxauto')
        if lib_name != 'wxautox':
            return jsonify({
                'code': 3001,
                'message': '当前库版本不支持朋友圈功能',
                'data': None
            }), 400

        # 调用Moments方法
        moments_wnd = wx_instance.Moments()

        return jsonify({
            'code': 0,
            'message': '进入朋友圈成功',
            'data': {
                'moments_window': str(moments_wnd) if moments_wnd else None
            }
        })
    except Exception as e:
        logger.error(f"进入朋友圈失败: {str(e)}")
        return jsonify({
            'code': 3001,
            'message': f'进入朋友圈失败: {str(e)}',
            'data': None
        }), 500

@moments_bp.route('/get-moments', methods=['GET'])
@require_api_key
def get_moments():
    """获取朋友圈内容 (Plus版)"""
    wx_instance = wechat_manager.get_instance()
    if not wx_instance:
        return jsonify({
            'code': 2001,
            'message': '微信未初始化',
            'data': None
        }), 400

    try:
        # 检查当前使用的库
        lib_name = getattr(wx_instance, '_lib_name', 'wxauto')
        if lib_name != 'wxautox':
            return jsonify({
                'code': 3001,
                'message': '当前库版本不支持朋友圈功能',
                'data': None
            }), 400

        # 获取参数
        n = request.args.get('n', 10, type=int)
        timeout = request.args.get('timeout', 10, type=int)

        # 获取朋友圈窗口
        moments_wnd = wx_instance.Moments()
        if not moments_wnd:
            return jsonify({
                'code': 3001,
                'message': '无法获取朋友圈窗口',
                'data': None
            }), 400

        # 获取朋友圈内容
        moments = moments_wnd.GetMoments(n=n, timeout=timeout)

        # 格式化朋友圈内容
        formatted_moments = []
        for moment in moments:
            formatted_moment = {
                'author': getattr(moment, 'author', ''),
                'content': getattr(moment, 'content', ''),
                'time': getattr(moment, 'time', ''),
                'images': getattr(moment, 'images', []),
                'likes': getattr(moment, 'likes', []),
                'comments': getattr(moment, 'comments', [])
            }
            formatted_moments.append(formatted_moment)

        return jsonify({
            'code': 0,
            'message': '获取朋友圈内容成功',
            'data': {
                'moments': formatted_moments
            }
        })
    except Exception as e:
        logger.error(f"获取朋友圈内容失败: {str(e)}")
        return jsonify({
            'code': 3001,
            'message': f'获取朋友圈内容失败: {str(e)}',
            'data': None
        }), 500

@moments_bp.route('/save-images', methods=['POST'])
@require_api_key
def save_moments_images():
    """保存朋友圈图片 (Plus版)"""
    wx_instance = wechat_manager.get_instance()
    if not wx_instance:
        return jsonify({
            'code': 2001,
            'message': '微信未初始化',
            'data': None
        }), 400

    data = request.get_json()
    moment_index = data.get('moment_index')
    save_path = data.get('save_path')

    if moment_index is None or not save_path:
        return jsonify({
            'code': 1002,
            'message': '缺少必要参数',
            'data': None
        }), 400

    try:
        # 检查当前使用的库
        lib_name = getattr(wx_instance, '_lib_name', 'wxauto')
        if lib_name != 'wxautox':
            return jsonify({
                'code': 3001,
                'message': '当前库版本不支持朋友圈功能',
                'data': None
            }), 400

        # 获取朋友圈窗口
        moments_wnd = wx_instance.Moments()
        if not moments_wnd:
            return jsonify({
                'code': 3001,
                'message': '无法获取朋友圈窗口',
                'data': None
            }), 400

        # 保存图片
        result = moments_wnd.SaveImages(moment_index, save_path)

        return jsonify({
            'code': 0,
            'message': '保存朋友圈图片成功',
            'data': {
                'moment_index': moment_index,
                'save_path': save_path,
                'result': str(result) if result else None
            }
        })
    except Exception as e:
        logger.error(f"保存朋友圈图片失败: {str(e)}")
        return jsonify({
            'code': 3001,
            'message': f'保存朋友圈图片失败: {str(e)}',
            'data': None
        }), 500

@moments_bp.route('/like', methods=['POST'])
@require_api_key
def like_moment():
    """点赞朋友圈 (Plus版)"""
    wx_instance = wechat_manager.get_instance()
    if not wx_instance:
        return jsonify({
            'code': 2001,
            'message': '微信未初始化',
            'data': None
        }), 400

    data = request.get_json()
    moment_index = data.get('moment_index')

    if moment_index is None:
        return jsonify({
            'code': 1002,
            'message': '缺少必要参数',
            'data': None
        }), 400

    try:
        # 检查当前使用的库
        lib_name = getattr(wx_instance, '_lib_name', 'wxauto')
        if lib_name != 'wxautox':
            return jsonify({
                'code': 3001,
                'message': '当前库版本不支持朋友圈功能',
                'data': None
            }), 400

        # 获取朋友圈窗口
        moments_wnd = wx_instance.Moments()
        if not moments_wnd:
            return jsonify({
                'code': 3001,
                'message': '无法获取朋友圈窗口',
                'data': None
            }), 400

        # 点赞
        result = moments_wnd.Like(moment_index)

        return jsonify({
            'code': 0,
            'message': '点赞成功',
            'data': {
                'moment_index': moment_index,
                'result': str(result) if result else None
            }
        })
    except Exception as e:
        logger.error(f"点赞失败: {str(e)}")
        return jsonify({
            'code': 3001,
            'message': f'点赞失败: {str(e)}',
            'data': None
        }), 500