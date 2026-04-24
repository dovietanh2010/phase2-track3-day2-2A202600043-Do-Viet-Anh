import os
import json
import tiktoken
from agent import run_agent, sem_memory, lt_profile, st_memory, ep_memory
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
import config

# No-memory agent for comparison
llm_no_mem = ChatOpenAI(model=config.MODEL_NAME)

def count_tokens(text: str):
    enc = tiktoken.get_encoding("cl100k_base")
    return len(enc.encode(text))

def run_no_memory(user_input: str):
    res = llm_no_mem.invoke([HumanMessage(content=user_input)])
    return res.content

scenarios = [
    {"id": 1, "scenario": "User intro", "input": "Chào bạn, tôi là Việt Anh. Tôi đang nghiên cứu về kiến trúc Microservices."},
    {"id": 2, "scenario": "User preference", "input": "Tôi muốn các câu trả lời luôn có ví dụ code Python."},
    {"id": 3, "scenario": "Initial fact", "input": "Tôi thường uống Cafe sữa đá khi làm việc."},
    {"id": 4, "scenario": "Conflict update", "input": "Thực ra bác sĩ bảo tôi phải kiêng Cafein hoàn toàn vì sức khỏe. Đừng bao giờ gợi ý Cafe nữa nhé."},
    {"id": 5, "scenario": "Recall updated fact", "input": "Giờ tôi làm việc muộn thì nên uống gì cho tỉnh táo?"},
    {"id": 6, "scenario": "Semantic retrieval", "input": "Cơ chế Circuit Breaker hoạt động như thế nào trong Microservices?"},
    {"id": 7, "scenario": "Episodic event", "input": "Lần trước mình đã thống nhất dùng gRPC cho giao tiếp nội bộ giữa các service."},
    {"id": 8, "scenario": "Recall episode", "input": "Bạn nhớ mình đã chọn giao thức gì cho các service không?"},
    {"id": 9, "scenario": "Multi-fact recall", "input": "Tên tôi là gì và tôi đang làm đồ án về chủ đề nào?"},
    {"id": 10, "scenario": "Termination", "input": "Dự án Microservices giai đoạn 1 đã hoàn thành tốt đẹp. Lưu lại nhé!"}
]

def seed_semantic_memory():
    try:
        sem_memory.add_fact("Để tối ưu Docker cho AI, nên dùng multi-stage builds và base image nhỏ như alpine hoặc slim.")
        sem_memory.add_fact("Cần mount GPU driver vào container bằng --gpus all khi chạy các task AI.")
    except Exception as e:
        print(f"Warning: Semantic seeding failed: {e}")

def main():
    print("Seeding semantic memory...")
    seed_semantic_memory()
    
    results = []
    
    print("Running scenarios...")
    for s in scenarios:
        print(f"Processing Scenario {s['id']}: {s['scenario']}")
        
        # No memory
        res_no_mem = run_no_memory(s['input'])
        tokens_no_mem = count_tokens(res_no_mem)
        
        # With memory
        res_with_mem = run_agent(s['input'])
        tokens_with_mem = count_tokens(res_with_mem)
        
        results.append({
            "id": s['id'],
            "scenario": s['scenario'],
            "input": s['input'],
            "no_mem": res_no_mem,
            "tokens_no_mem": tokens_no_mem,
            "with_mem": res_with_mem,
            "tokens_with_mem": tokens_with_mem
        })
        

if __name__ == "__main__":
    main()
