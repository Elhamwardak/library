from django.urls import path
from . import views

urlpatterns = [
    path('',views.Index,name='index'),
    path('book-discription/<str:id>/',views.bookDiscriptions,name='book-discription'),

    path('admin-page/', views.Admin, name="admin-page"),
    path('books-management/', views.book_list, name="books-management"),
    path('users-management/', views.user_list, name="users-management"),
    path('book_list/', views.booklisttostudnet,name='book-list'),
    path('contact_us/', views.contactUs,name='contact-us'),
    path('message/',views.Message,name="message"),
    path('delete/<str:id>/',views.deletemessage,name="delete-message"),



    path('add-book/', views.add_book, name="add-book"),
    path('update-book/<str:id>/', views.Update_book, name="update-book"),
    path('delete-book/<str:id>', views.Delete_book, name="delete-book"),
    path('issue-book/', views.issue_book, name="issue-book"),
    path('issue-book-to-student/',views.issue_book_to_student,name="issue-book-to-student"),
    path('view-issuebook/<str:books>', views.ViewIssueBook, name="view-issuebook"),
    path('books-not-return/', views.booksnotreturnyet, name="books-not-return"),
    path('category/',views.categorylist, name="category-list"),
    path('add_category/', views.add_category, name='add_category'),
    path('update-category/<str:id>/',views.update_category,name='update-category'),
    path('delete-category/<str:id>', views.delete_category, name="delete-category"),
    path('Author/',views.authorslist, name="author-list"),
    path('add_author/', views.add_author, name='add_author'),
    path('update-author/<str:id>/',views.update_author,name='update-author'),
    path('delete-author/<str:id>', views.delete_author, name="delete-author"),

    path('studentlist/',views.StudentList, name ="studentlist"),
    path('teacherlist/',views.TeacherList, name ="teacherlist"),


    path('add-user/', views.add_user, name="add-user"),
    path('update-user/<str:id>/', views.Update_user, name="update-user"),
    path('delete-user/<str:id>/', views.Delete_user, name="delete-user"),

    path('login-page/', views.LoginPage, name="login-page"),
    path('logout/', views.logoutUser, name="logout"),

    path('view-issue-to-student/', views.issuebook_to_student, name="view-issue-to-student"),

    path('profile/', views.user_profile, name="user-profile"),
    path('update-profile/<str:id>/',views.Update_profile, name="update-profile"),

    path('returned-date/<str:id>/', views.return_date, name="return-date"),

    path('like/<int:book_id>/<int:like>', views.like, name="like"),
    path('favourite/<int:book_id>/<int:favourite>', views.favourite, name="favourite"),
    path('my-favourites/', views.MyFavourites, name="my-favourites"),

    path('change-password/', views.ChangePassword, name="change-password"),



]
