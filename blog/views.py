from django.shortcuts import render, get_object_or_404, redirect
from django.template.defaultfilters import title
from .forms import CommentForm
from .models import Post,Comment
from .forms import PostForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .forms import ImageForm
from .models import Image


def post_list(request):
    query=request.GET.get('q')
    posts = Post.objects.all()

    if query:
        posts=posts.filter( Q(title__icontains=query) | Q(content__icontains=query) )


    paginator = Paginator(posts, 5)  # 5 posts per page
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)
    return render(request, 'blog/post_list.html', {'posts': posts})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.all()

    if request.method == 'POST':
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.post = post
                comment.author = request.user
                comment.save()
                messages.success(request, "Comment added.")
                return redirect('blog:post_detail', pk=post.pk)

    else:
        form = CommentForm()

    return render(request, 'blog/post_detail.html', {
        'post': post,
        'comments': comments,
        'form': form
    })


@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'Post created successfully!')
            return redirect('blog:post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_form.html', {'form': form})


@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user:
        messages.error(request, "You are not allowed to edit this post.")
        return redirect('blog:post_detail', pk=pk)

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post updated successfully!')
            return redirect('blog:post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_form.html', {'form': form})


@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user:
        messages.error(request, "You are not allowed to delete this post.")
        return redirect('blog:post_detail', pk=pk)

    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Post deleted.')
        return redirect('blog:post_list')
    return render(request, 'blog/post_confirm_delete.html', {'post': post})



@login_required
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, author=request.user)
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            messages.success(request, "Comment updated successfully.")
            return redirect('blog:post_detail', pk=comment.post.pk)
    else:
        form = CommentForm(instance=comment)
    return render(request, 'blog/edit_comment.html', {
        'form': form,
        'comment': comment
        })

@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, author=request.user)
    if request.method == 'POST':
        comment.delete()
        messages.success(request, "Comment deleted.")
        return redirect('blog:post_detail', pk=comment.post.pk)
    return render(request, 'blog/delete_comment.html', {'comment': comment})


@login_required
def upload_image(request):
    if request.method =='POST':
        form = ImageForm(request.POST,request.FILES)
        if form.is_valid():
            image=form.save(commit=False)
            image.user=request.user
            image.save()
            return redirect('blog:image_gallery')

    else:
        form = ImageForm()
    return render(request,'blog/upload_image.html',{'form':form})



def image_gallery(request):
    images = Image.objects.all().order_by('-created_at')
    paginator = Paginator(images, 6)
    page = request.GET.get('page')
    images = paginator.get_page(page)
    return render(request, 'blog/image_gallery.html', {'images': images})

def image_detail(request, id):
    image = get_object_or_404(Image, id=id)
    return render(request, 'blog/image_detail.html', {'image': image})

@login_required
def image_delete(request, id):
    image = get_object_or_404(Image, id=id, user=request.user)
    image.delete()
    return redirect('blog:image_gallery')


