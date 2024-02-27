from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.utils.text import slugify
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView

from apps.books.forms import AddBookReviewForm, AddAuthorForm, UpdateAuthorForm, BookForm
from apps.books.models import Book, Author, BookGenre, BookReview
from apps.users.models import User


class BookListView(ListView):
    model = Book
    context_object_name = "books"
    template_name = "books/book_list.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        param = self.request.GET.get('q')
        if param:
            quertset = queryset.filter(title__icontains=param)
        return queryset

    # def get_context_data(self, *, object_list=None, **kwargs):
    #     context = super().get_context_data(object_list=object_list, **kwargs)
    #     context["form"] = SearchForm()
    #     return context


class BookDetailView(DetailView):
    model = Book
    # pk_url_kwarg = "slug"
    slug_url_kwarg = "slug"
    context_object_name = "book"
    template_name = "books/book_detail.html"


class AuthorListView(ListView):
    model = Author
    context_object_name = "authors"
    template_name = "books/author_list.html"


class AuthorDetailView(DetailView):
    model = Author
    context_object_name = "author"
    template_name = "books/author_detail.html"


class GenreListView(ListView):
    model = BookGenre
    context_object_name = "genres"
    template_name = "books/genre_list.html"


class GenreDetailView(DetailView):
    model = BookGenre
    slug_field = 'name'
    slug_url_kwarg = 'name'
    context_object_name = "genre"
    template_name = "books/genre_detail.html"


class AddReviewView(View):
    def post(self, request, pk):
        book = Book.objects.get(id=pk)
        user = User.objects.get(username=request.user.username)
        form = AddBookReviewForm(request.POST)
        if form.is_valid():
            BookReview.objects.create(
                user=user,
                book=book,
                body=form.cleaned_data.get("body"),
                rating=form.cleaned_data.get("rating")
            )
            return redirect(reverse("books:book-detail", kwargs={"slug": book.slug}))
        else:
            context = {
                "book": book,
                "form": form
            }
            return render(request, "books/book_detail.html", context=context)


class AuthorCreateView(LoginRequiredMixin, CreateView):
    model = Author
    form_class = AddAuthorForm
    # fields = ("first_name", "last_name", "birth_place", "birth_date", "avatar", "website", "about")
    template_name = "books/author_form.html"
    success_url = reverse_lazy("books:author_list")


class AuthorUpdateView(LoginRequiredMixin, UpdateView):
    model = Author
    form = UpdateAuthorForm
    fields = ("first_name", "last_name", "birth_date", "birth_place", "avatar", "website", "about")
    template_name = "books/author_form.html"


class BookCreateView(LoginRequiredMixin, View):
    def post(self, request):
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = Book.objects.create(
                title=form.cleaned_data["title"],
                description=form.cleaned_data["description"],
                cover=form.cleaned_data["cover"],
                published=form.cleaned_data["published"],
                isbn=form.cleaned_data["isbn"],
                language=form.cleaned_data["language"],
                page=form.cleaned_data["page"]
            )
            book.genre.set(form.cleaned_data["genre"])
            book.authors.set(form.cleaned_data["authors"])
            book.slug = slugify(book.title)
            book.save()

            messages.success(request, "Book created")
            return redirect("books:book_list")
        else:
            form = BookForm(request.POST)
            return render(request, "books/book_form.html", {"form": form})

    def get(self, request):
        form = BookForm()
        return render(request, "books/book_form.html", {"form": form})


class BookUpdateView(UpdateView):
    model = Book
    form_class = BookForm
    template_name = "books/book_form.html"
