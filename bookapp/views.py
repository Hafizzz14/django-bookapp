from django.shortcuts import render, redirect, get_object_or_404
from .models import Book
from .forms import BookForm

# 1. Login dan Logout (Session dan Cookie)
def login_view(request):
    error = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember = request.POST.get('remember')

        # Simulasi login
        if username == 'admin' and password == '123':
            request.session['is_logged_in'] = True
            request.session['username'] = username

            response = redirect('book_list')
            if remember:
                response.set_cookie('last_login', username, max_age=3600)
            return response
        else:
            error = "Username atau Password salah!"
    return render(request, 'login.html', {'error': error})

def logout_view(request):
    request.session.flush()
    response = redirect('login')
    response.delete_cookie('last_login')
    return response

# 2. Read (Daftar Buku)
def book_list(request):
    if not request.session.get('is_logged_in'): return redirect('login')

    books = Book.objects.all()
    request.session['last_page'] = 'book_list' # Menyimpan session info

    response = render(request, 'book_list.html', {'books': books, 'username': request.session.get('username')})
    response.set_cookie('visited', 'yes', max_age=3600) # Menyimpan cookie info
    return response

# 3. Create (Tambah Buku)
def book_create(request):
    if not request.session.get('is_logged_in'): return redirect('login')

    form = BookForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('book_list')
    return render(request, 'book_form.html', {'form': form, 'title': 'Tambah Buku'})

# 4. Update (Edit Buku)
def book_update(request, id):
    if not request.session.get('is_logged_in'): return redirect ('login')

    book = get_object_or_404(Book, id=id)
    form = BookForm(request.POST or None, instance=book)
    if form.is_valid():
        form.save()
        return redirect('book_list')
    return render(request, 'book_form.html', {'form': form, 'title': 'Edit Buku'})

# 5. Delete (Hapus Buku)
def book_delete(request, id):
    if not request.session.get('is_logged_in'): return redirect('login')
    
    book = get_object_or_404(Book, id=id)
    if request.method == 'POST':
        book.delete()
        return redirect('book_list')
    return render(request, 'book_delete.html', {'book': book})

# 6. Info Session dan Cookie
def info(request):
    if not request.session.get('os_logged_in'): return redirect('login')

    last_page = request.session.get('last_page', 'Belum Ada')
    visited = request.COOKIES.get('visited', 'Belum Ada')
    return render(request, 'info.html', {'last_page': last_page, 'visited': visited})
