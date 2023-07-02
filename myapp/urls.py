from django.urls import path
from . import views

urlpatterns = [
    path('admin-page/', views.Admin, name="admin-page"),
    path('books-management/', views.book_list, name="books-management"),
    path('users-management/', views.user_list, name="users-management"),
    path('book_list/', views.booklisttostudnet,name='book-list'),


    path('add-book/', views.add_book, name="add-book"),
    path('update-book/<str:id>/', views.Update_book, name="update-book"),
    path('delete-book/<str:id>', views.Delete_book, name="delete-book"),
    path('issue-book/', views.issue_book, name="issue-book"),
    path('issue-book-to-student/',views.issue_book_to_student,name="issue-book-to-student"),
    path('view-issuebook/<str:books>', views.ViewIssueBook, name="view-issuebook"),
    path('books-not-return/', views.booksnotreturnyet, name="books-not-return"),
    path('category/',views.categorylist, name="category-list"),
    path('add_category/', views.add_category, name='add_category'),
    

    path('add-user/', views.add_user, name="add-user"),
    path('update-user/<str:id>/', views.Update_user, name="update-user"),
    path('delete-user/<str:id>', views.Delete_user, name="delete-user"),

    path('', views.LoginPage, name="login-page"),
    path('register-page/', views.registerPage, name="register-page"),
    path('logout/', views.logoutUser, name="logout"),

    path('view-issue-to-student/', views.issuebook_to_student, name="view-issue-to-student"),
    path('profile/', views.user_profile, name="user-profile"),
    path('returned-date/<str:id>/', views.return_date, name="return-date"),

  


]
