from django.shortcuts import render, get_object_or_404, redirect
from .forms import BoardForm, CommentForm
from .models import Board, Comment
from django.utils import timezone

# Create your views here.
def post(request):
    if request.method == 'POST':
        form = BoardForm(request.POST) #BoardForm으로부터 받은 데이터를 처리하기 위한 인스턴스 생성
        if form.is_valid(): #폼 검증 메소드
            board = form.save(commit = False) #board 오브젝트를 form으로부터 가져오지만 실제로 DB반영은 하지 않는다.
            board.update_date=timezone.now()
            board.save()
            return redirect("show") #url의 name을 경로대신 입력한다.

    else:
        form = BoardForm() #forms.py의 BoardForm 클래스의 인스턴스
        return render(request, 'post.html',{'form' : form})


def detail(request, board_id):
    board_detail = get_object_or_404(Board, pk=board_id)
    return render(request, 'detail.html', {'board':board_detail})

def edit(request, pk): #url에서 pk를 받아서 처리
    board = get_object_or_404(Board, pk=pk)
    if request.method == 'POST':
        form = BoardForm(request.POST, instance=board) 
        if form.is_valid(): #폼 검증 메소드
            board = form.save(commit = False) 
            board.update_date=timezone.now()
            board.save()
            return redirect("show") 

    else:
        form = BoardForm(instance=board) 
        return render(request, 'edit.html',{'form' : form})

        #edit이 post와 다른 점
        #url로부터 추가로 pk매개변수를 받아서 처리
        #수정하고자 하는 글의 Board모델 인스터스로 가져온다.

def delete(request, pk):
    board = Board.objects.get(id=pk)
    board.delete()
    return redirect('show')

def show(request): #글을 최신순으로
    boards=Board.objects.order_by('-id') #id의 반대 순서로 정렬하라
    return render(request, 'show.html', {'boards':boards})

def comment(request, board_pk):
        board = Board.objects.get(pk=board_pk)
        if request.method == "POST":
                board = get_object_or_404(Board,pk=board_pk)
                message = request.POST.get('message')

        else:
            form = CommentForm() 
            return render(request, 'comment.html',{'form' : form})
