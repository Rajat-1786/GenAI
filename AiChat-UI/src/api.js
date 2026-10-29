async function post(path, body) {
  let res
  try {
    res = await fetch(path, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    })
  } catch {
    throw new Error('Cannot reach the server. Please try again shortly.')
  }

  const data = await res.json().catch(() => ({}))
  if (!res.ok) {
    // FastAPI returns either {detail: "msg"} or {detail: [{msg, ...}]} for validation errors.
    const detail = Array.isArray(data.detail)
      ? data.detail.map((d) => d.msg).join(', ')
      : data.detail
    throw new Error(detail || `Request failed (${res.status})`)
  }
  return data
}

export function signup({ name, email, password, confirm }) {
  return post('/auth/signup', {
    user_name: name,
    email,
    password,
    confirm_password: confirm,
  })
}
