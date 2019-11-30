# from functools import wraps
# from flask_login import current_user
#
#
# def admin_login_required(f):
#     @wraps(f)
#     def auth_required(*args, **kwargs):
#         # user = current_user.filter_by(id).first()
#         if not current_user.is_admin == 'True':
#             return "You neeed to be an administrator to do that, 401"
#         return f(*args, **kwargs)
#     return auth_required()
