import json

import pandas as pd
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from langchain.agents.agent_types import AgentType
from langchain.chat_models import ChatOpenAI
from langchain_experimental.agents.agent_toolkits import \
    create_pandas_dataframe_agent

# Create your views here.
from .models import File, Prompts


@login_required(login_url='accounts:loginUser', redirect_field_name='next')
def home(request):
    template_name = "pages/index.html"
    if request.method == 'POST':

        file = request.FILES.get('file')

        if file is None:
            messages.info(request, 'No file selected')
            return redirect('core:home')

        if not file.name.endswith('.csv'):
            messages.info(request, 'File is not CSV type')
            return redirect('core:home')

        user = request.user
        filename = file.name
        File.objects.create(file=file, namefile=filename, user=user)
        return redirect(f'question' + '/' + str(File.objects.last().id))

    if request.user.is_authenticated:
        files = File.objects.filter(user=request.user)
        context = {
            'files': files
        }
        return render(request, template_name, context)

    return render(request, template_name)


@login_required(login_url='accounts:loginUser', redirect_field_name='next')
def question(request, id):
    template_name = "pages/questions.html"
    prompts = Prompts.objects.filter(file=id, user=request.user)

    context = {
        'prompts': prompts
    }

    return render(request, template_name, context)


@login_required(login_url='accounts:loginUser', redirect_field_name='next')
@csrf_exempt
def query(request, id):
    if request.method == "POST":
        try:
            # Lendo o arquivo csv
            file_instance = File.objects.get(id=id)
            file = file_instance.file.open()

            data = pd.read_csv(file, sep=',', header=0)
            df = pd.DataFrame(data)

            promptsStatic = Prompts.objects.filter(file=id, user=request.user)

            promptSelected = []
            for prompt in promptsStatic:
                if prompt.selected:
                    promptSelected.append(prompt)

            # Criando o agente com o dataframe
            agent = create_pandas_dataframe_agent(
                ChatOpenAI(temperature=0.2, model="gpt-3.5-turbo"),
                df,
                verbose=True,
                agent_type=AgentType.OPENAI_FUNCTIONS,
            )
            # Obter a consulta do corpo da solicitação
            data = json.loads(request.body.decode("utf-8"))
            query = data["input"]

            query = '\n'.join(
                [selected_prompt.prompt for selected_prompt in promptSelected]) + '\n' + query

            # print(query)

            # Executar a consulta no agente
            response = agent.run(query)

            # Verifique se a resposta é uma string
            if isinstance(response, str):
                # Se for, defina a fonte como vazia, pois não há uma fonte formatada
                source = ""
            else:
                # Caso contrário, obtenha a fonte formatada
                source = response.get_formatted_sources()

            # Retornar a consulta, resposta e fonte como JSON
            return JsonResponse({'success': True, 'query': query, 'response': str(response), 'source': source})
        except Exception as e:
            print(e)
            return JsonResponse({'success': False, 'error': str(e)}, status=500)


@login_required(login_url='accounts:loginUser', redirect_field_name='next')
def delete(request, id):
    if request.method == "POST":
        file = File.objects.filter(id=id, user=request.user).first()
        file.delete()
        return redirect('core:home')
