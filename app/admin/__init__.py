from .view import admin, SelectCategory, LoginView, HumanCreateOrEdit, HumanList, DelHuman, StudioList, DelStudio, \
    StudioCreateOrEdit, NewsList, DelNews, NewsCreateOrEdit, UploadImages, Images_list, DelImg

admin.add_url_rule('/login/', view_func=LoginView.as_view('login'))
admin.add_url_rule('/select-category/', view_func=SelectCategory.as_view('select_category'))

img_list = Images_list.as_view('img_list')  # 分页功能，两个注册蓝图公用一个类和终节点
admin.add_url_rule('/images/', view_func=img_list)
admin.add_url_rule('/images/<int:page>', view_func=img_list)
admin.add_url_rule('/images/upload/', view_func=UploadImages.as_view('upload_img'))
admin.add_url_rule('/del/images/<int:id>', view_func=DelImg.as_view('del_img'))

humans_list = HumanList.as_view('humans_list')  # 分页功能，两个注册蓝图公用一个类和终节点
admin.add_url_rule('/humans/', view_func=humans_list)
admin.add_url_rule('/humans/<int:page>', view_func=humans_list)
admin.add_url_rule('/del-humans/<int:id>/', view_func=DelHuman.as_view('del_humans'))
admin.add_url_rule('/humans/create/', view_func=HumanCreateOrEdit.as_view('humans_create'))
admin.add_url_rule('/humans/edit/<int:id>/', view_func=HumanCreateOrEdit.as_view('humans_edit'))

studio_list = StudioList.as_view('studio_list')
admin.add_url_rule('/studios/', view_func=studio_list)
admin.add_url_rule('/studios/<int:page>', view_func=studio_list)
admin.add_url_rule('/del-studios/<int:id>/', view_func=DelStudio.as_view('del_studios'))
admin.add_url_rule('/studios/create/', view_func=StudioCreateOrEdit.as_view('studios_create'))
admin.add_url_rule('/studios/edit/<int:id>/', view_func=StudioCreateOrEdit.as_view('studios_edit'))

news_list = NewsList.as_view('news_list')
admin.add_url_rule('/news/', view_func=news_list)
admin.add_url_rule('/news/<int:page>', view_func=news_list)
admin.add_url_rule('/del-news/<int:id>/', view_func=DelNews.as_view('del_news'))
admin.add_url_rule('/news/create/', view_func=NewsCreateOrEdit.as_view('news_create'))
admin.add_url_rule('/news/edit/<int:id>/', view_func=NewsCreateOrEdit.as_view('news_edit'))
