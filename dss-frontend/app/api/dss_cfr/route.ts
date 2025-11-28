export async function POST(req: Request) {
  const body = await req.json();
  const res = await fetch("http://127.0.0.1:8000/predict_cfr", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  return Response.json(await res.json());
}
