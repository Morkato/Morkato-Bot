export function Snowflake({
  worker = 1,
  epoch = 1672531200000,
  bits = 8,
  seq = 24
}: {
  worker?: number
  epoch?: number
  bits?: number
  seq?: number
}) {
  function generate(ts?: number): string {
    const timestamp = BigInt((ts || Date.now()) - epoch)

    return ((timestamp << BigInt(bits + seq)) | (BigInt(worker) << BigInt(seq))).toString()
  }

  function created_at(id: string): number {
    const timestamp = (BigInt(id) >> BigInt(bits + seq)) + BigInt(epoch)

    return Number(timestamp);
  }

  return { generate, created_at };
}

const snowflake = Snowflake({})

export function uuid(ts?: number) {
  return snowflake.generate(ts)
}

export function created_at(id: string): number {
  return snowflake.created_at(id)
}