const base = "http://localhost:8000/api";

export async function get<T>(path: string): Promise<T> {
  const response = await fetch(`${base}${path}`);
  if (!response.ok) throw new Error("FlowTask API 请求失败");
  return response.json() as Promise<T>;
}

export async function post<T>(path: string, payload: unknown): Promise<T> {
  const response = await fetch(`${base}${path}`, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(payload) });
  if (!response.ok) throw new Error("FlowTask API 请求失败");
  return response.json() as Promise<T>;
}
