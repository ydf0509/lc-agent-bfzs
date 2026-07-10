import sqlite3, json

conn = sqlite3.connect('bfzs_data.db')
cur = conn.cursor()

# 查有 TOOL 标记的消息（non-subagent对照组）
cur.execute("""
    SELECT m.session_id, m.role, m.content, m.tool_calls, m.created_at
    FROM chat_ui_messages m
    WHERE m.role = 'assistant' AND m.content LIKE '%TOOL:%'
    ORDER BY m.created_at DESC LIMIT 3
""")
rows = cur.fetchall()
print("Messages with TOOL markers (for comparison):")
for r in rows:
    tc_raw = r[3]
    try:
        tc = json.loads(tc_raw) if tc_raw else None
        tc_str = json.dumps(tc)[:200] if tc else "null"
    except:
        tc_str = str(tc_raw)[:100]
    print(f"\n=== sess={r[0][:16]}... at={r[4]} ===")
    print(f"content ({len(r[2])} chars): {r[2][:300]}")
    print(f"tool_calls: {tc_str}")

# 查没有TOOL标记但有双THINK的消息
cur.execute("""
    SELECT m.session_id, m.role, m.content, m.tool_calls, m.created_at
    FROM chat_ui_messages m
    WHERE m.role = 'assistant' 
    AND m.content NOT LIKE '%TOOL:%' 
    AND m.content LIKE '%THINK_END%THINK_START%'
    ORDER BY m.created_at DESC LIMIT 3
""")
rows = cur.fetchall()
print("\n\nMessages with double-think but NO TOOL marker:")
for r in rows:
    tc_raw = r[3]
    tc_str = json.dumps(json.loads(tc_raw))[:200] if tc_raw else "null"
    print(f"\n=== sess={r[0][:16]}... at={r[4]} ===")
    print(f"content ({len(r[2])} chars): {r[2][:300]}")
    print(f"tool_calls: {tc_str}")

conn.close()
