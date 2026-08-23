from django.shortcuts import render
from core.models import Comment
from groq import Groq
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import os


def home_view(request, author_username=None):
    comments = Comment.objects.filter(status=True)
    if author_username:
        comments = comments.filter(author__username=author_username)
    context = {"comments": comments}
    return render(request, "core/home.html", context)


def about_view(request):
    return render(request, "core/about.html")


def contact_view(request):
    return render(request, "core/contact.html")


@csrf_exempt
def ai_resume_coach(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_message = data.get("message")

            # >>> کلید API و کلاینت رو اینجا بساز <<<
            api_key = os.environ.get("API_KEY")
            if not api_key:
                return JsonResponse(
                    {"reply": "کلید API تنظیم نشده. لطفاً با پشتیبان تماس بگیرید."},
                    status=500
                )
            client = Groq(api_key=api_key)

            # فراخوانی مدل Groq
            completion = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {
                        "role": "system",
                        "content": "تو 'مربی هوشمند رزومینو' هستی. وظیفه تو تحلیل رزومه و مشاوره شغلی به کاربران است. به فارسی پاسخ بده و بسیار صمیمی و حرفه‌ای باش.",
                    },
                    {"role": "user", "content": user_message},
                ],
                temperature=0.7,
                max_tokens=1024,
            )

            ai_reply = completion.choices[0].message.content
            return JsonResponse({"reply": ai_reply})

        except Exception as e:
            print(f"Groq Error: {e}")
            return JsonResponse(
                {"reply": "اوپس! ارتباطم با مغز متفکرم قطع شده. دوباره امتحان کن."},
                status=500,
            )

    return JsonResponse({"error": "Invalid request"}, status=400)