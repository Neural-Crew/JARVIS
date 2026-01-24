export async function* parseTextStream(stream) {
  const reader = stream
    .pipeThrough(new TextDecoderStream())
    .getReader();

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    if (value) yield value;
  }
}
