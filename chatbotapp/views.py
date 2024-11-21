from django.shortcuts import redirect, render
from triprecommendator.settings import GENERATIVE_AI_KEY
from chatbotapp.models import ChatMessage
import google.generativeai as genai
import markdown


def send_message(request):
    md = markdown.Markdown(extensions=["extra"])
    if request.method == "POST":
        genai.configure(api_key=GENERATIVE_AI_KEY)
        model = genai.GenerativeModel("gemini-1.5-flash")

        user_message = request.POST.get("user_message")
        text_content = model.generate_content(user_message)

        bot_response = md.convert(str(text_content.candidates[0].content.parts[0].text))
        ChatMessage.objects.create(user_message=user_message, bot_response=bot_response)
    return redirect("list_messages")


def list_messages(request):
    messages = ChatMessage.objects.all()
    return render(request, "chatbot/list_messages.html", {"messages": messages})
