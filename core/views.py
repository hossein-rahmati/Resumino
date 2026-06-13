from django.db.models.manager import BaseManager
from django.shortcuts import render
from core.models import Comment
from groq import Groq
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import os


# Create your views here.
def home_view(request, author_username=None):
    comments = Comment.objects.filter(status=True)
    if author_username:
        posts: BaseManager[Comment] = posts.filter(author__username=author_username)
    context = {'comments': comments}
    return render(request, "core/home.html", context)


def about_view(request):
    return render(request, 'core/about.html')


def contact_view(request):
    return render(request, 'core/contact.html')


API_KEY = os.environ.get("API_KEY")
client = Groq(api_key="")
try:
    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": "Hi"}]
    )
    print("اتصال برقرار است:", completion.choices[0].message.content)
except Exception as e:
    print("خطای اتصال:", e)


@csrf_exempt
def ai_resume_coach(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_message = data.get("message")

            # فراخوانی مدل Groq
            completion = client.chat.completions.create(
                model="llama-3.1-8b-instant",  # مدل فوق سریع و رایگان
                messages=[
                    {
                        "role": "system",
                        "content": "تو 'مربی هوشمند رزومینو' هستی. وظیفه تو تحلیل رزومه و مشاوره شغلی به کاربران است. به فارسی پاسخ بده و بسیار صمیمی و حرفه‌ای باش."
                    },
                    {"role": "user", "content": user_message}
                ],
                temperature=0.7,
                max_tokens=1024,
            )

            ai_reply = completion.choices[0].message.content
            return JsonResponse({"reply": ai_reply})

        except Exception as e:
            print(f"Groq Error: {e}")  # برای دیدن خطا در ترمینال
            return JsonResponse({"reply": "اوپس! ارتباطم با مغز متفکرم قطع شده. دوباره امتحان کن."}, status=500)

    return JsonResponse({"error": "Invalid request"}, status=400)
