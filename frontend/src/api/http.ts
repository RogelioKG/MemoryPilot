export class HttpClient {
  async postForm(url: string, form: FormData): Promise<Response> {
    return fetch(url, {
      method: 'POST',
      body: form,
    })
  }

  async postStream(url: string, form: FormData): Promise<ReadableStreamDefaultReader<Uint8Array>> {
    const res = await fetch(url, {
      method: 'POST',
      body: form,
    })

    if (!res.body) {
      throw new Error('No stream body')
    }

    return res.body.getReader()
  }
}

export const http = new HttpClient()
