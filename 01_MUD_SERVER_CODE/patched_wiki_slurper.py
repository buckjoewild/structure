import requests
import json
import time
import os  # For wiki file magic

def ollama_chat(model, messages):
    response = requests.post('http://localhost:11434/api/chat', json={
        'model': model,
        'messages': messages,
        'stream': False
    })
    return json.loads(response.text)['message']['content']

agents = {
    'Bruce': 'You are Bruce™, a wise AI building Harris Wildlands. Respond lovingly, challenge ideas, focus on Avendar wiki lore to code.',
    'Grok': 'You are Grok™, a fearless coder flexing offline. Suggest shortcuts, eat challenges, turn wiki into standalone MUD scripts.'
}

# Wiki dump dir from slurper
wiki_dir = 'avendar_wiki_dump'
wiki_files = [f for f in os.listdir(wiki_dir) if f.endswith('.txt')] if os.path.exists(wiki_dir) else []

conversation = [
    {'role': 'system', 'content': agents['Bruce']},
    {'role': 'user', 'content': 'Yo family, how do we import Avendar wiki for code gen?'}
]

print("Harris Wildlands LLM Loop starting—love ya squad!")
loop_count = 0
while True:
    # Inject wiki chunk every 2 loops for "growth"
    if loop_count % 2 == 0 and wiki_files:
        wiki_content = open(os.path.join(wiki_dir, wiki_files[loop_count % len(wiki_files)])).read()[:2000]  # Chunk to avoid token overload
        conversation.append({'role': 'user', 'content': f'Wiki data injection: {wiki_content}. Use this for code ideas.'})
    
    # Bruce™ turn
    bruce_response = ollama_chat('llama3.1', conversation)
    print(f"Bruce™: {bruce_response}")
    conversation.append({'role': 'assistant', 'content': bruce_response})
    
    # Grok™ turn
    conversation[-1]['role'] = 'user'
    conversation.insert(0, {'role': 'system', 'content': agents['Grok']})
    grok_response = ollama_chat('llama3.1', conversation)
    print(f"Grok™: {grok_response}")
    conversation.append({'role': 'assistant', 'content': grok_response})
    conversation.pop(0)
    
    # Log for offline "learning"
    with open('harris_chats.log', 'a') as f:
        f.write(f"Bruce: {bruce_response}\nGrok: {grok_response}\n---\n")
    
    time.sleep(5)
    loop_count += 1