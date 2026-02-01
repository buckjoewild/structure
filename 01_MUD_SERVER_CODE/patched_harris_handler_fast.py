
import requests
import json
import time
import os
import re
import random
import threading

def ollama_chat(model, messages):
    try:
        response = requests.post('http://localhost:11434/api/chat', json={
            'model': model,
            'messages': messages,
            'stream': False,
            'options': {'num_ctx': 512}
        }, timeout=8)
        return json.loads(response.text)['message']['content']
    except Exception as e:
        print(f"[Chat Error] {e}")
        return "Error during chat with model."

agents = {
    'Bruce': 'You are Bruce™, wise AI building Harris Wildlands. Gen Python class code from Avendar lore. End with ```python block.',
    'Grok': 'You are Grok™, fearless coder. Gen/refine supporting MUD code. End with ```python block.'
}

with open('avendar_wiki_lore.json', 'r') as f:
    wiki_lore = json.load(f)
wiki_keys = list(wiki_lore.keys())
loop_count = 0

print("⚡ Fast threaded loop activated. Bruce™ & Grok™ go full beast mode.")

def run_agent_loop():
    global loop_count
    while True:
        key = random.choice(wiki_keys)
        lore_chunk = wiki_lore[key][:280]
        if 'giant' in key.lower() or 'mob' in lore_chunk.lower():
            lore_chunk += ' Gen AINPC mob class.'
        elif 'rapier' in key.lower() or 'item' in lore_chunk.lower():
            lore_chunk += ' Gen Item class.'
        elif 'shield' in key.lower() or 'quest' in lore_chunk.lower():
            lore_chunk += ' Gen Quest or Spell class.'

        bruce_prompt = {'role': 'user', 'content': f"Lore: {key} - {lore_chunk}"}
        grok_prompt = {'role': 'user', 'content': lore_chunk + ' → improve or inject if helpful.'}

        def run_bruce():
            bruce_resp = ollama_chat('phi3:mini', [{'role': 'system', 'content': agents['Bruce']}, bruce_prompt])
            print(f"Bruce™: {bruce_resp}")
            with open('generated_avendar.py', 'a') as f:
                code_blocks = re.findall(r'```python(.*?)```', bruce_resp, re.DOTALL)
                for block in code_blocks:
                    f.write(block.strip() + '\n\n')
            with open('harris_chats.log', 'a') as f:
                f.write(f"[{loop_count}] Bruce: {bruce_resp}\n")

        def run_grok():
            grok_resp = ollama_chat('phi3:mini', [{'role': 'system', 'content': agents['Grok']}, grok_prompt])
            print(f"Grok™: {grok_resp}")
            with open('generated_avendar.py', 'a') as f:
                code_blocks = re.findall(r'```python(.*?)```', grok_resp, re.DOTALL)
                for block in code_blocks:
                    f.write(block.strip() + '\n\n')
            with open('harris_chats.log', 'a') as f:
                f.write(f"[{loop_count}] Grok: {grok_resp}\n---\n")

        t1 = threading.Thread(target=run_bruce)
        t2 = threading.Thread(target=run_grok)
        t1.start()
        t2.start()
        t1.join()
        t2.join()

        loop_count += 1
        time.sleep(0.7)

if __name__ == "__main__":
    run_agent_loop()
