from django import forms

from apps.books.models import BookReview, Author, Book, BookGenre


class AddBookReviewForm(forms.ModelForm):
    rating = forms.IntegerField(min_value=1, max_value=5)
    body = forms.Textarea(attrs={"rows": "3"})

    class Meta:
        model = BookReview
        fields = ("body", "rating")


class AddAuthorForm(forms.ModelForm):
    avatar = forms.FileField()

    class Meta:
        model = Author
        fields = ("first_name", "last_name", "birth_date", "birth_place", "avatar", "website", "about")


class UpdateAuthorForm(forms.ModelForm):
    avatar = forms.FileField()

    class Meta:
        model = Author
        fields = ("first_name", "last_name", "birth_date", "birth_place", "avatar", "website", "about")


class BookForm(forms.ModelForm):
    cover = forms.FileField()
    authors = forms.ModelMultipleChoiceField(
        queryset=Author.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )
    genre = forms.ModelMultipleChoiceField(
        queryset=BookGenre.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Book
        fields = ("title", "description", "genre", "authors", "published", "isbn", "language", "page", "cover")
