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
  const maxSeq = (1 << seq) - 1
  const maxWorker = ((1 << bits) * worker) - 1

  function generate(ts?: number): string {
    const timestamp = BigInt((ts || Date.now()) - epoch)

    return ((timestamp << BigInt(bits + seq)) | (BigInt(worker) << BigInt(seq))).toString()
  }

  function isValid(id: string): boolean {
    const isValidExpression = /^[0-9]+$/.test(id)

    if (!isValidExpression) {
      return false;
    }

    const idInt = BigInt(id)

    const idSeq = Number(idInt & BigInt(maxSeq))
    const idWorker = Number((idInt >> BigInt(seq)) & BigInt(maxWorker))

    const isValidWorkerId = idWorker >= 0 && idWorker <= maxWorker
    const isValidSequence = idSeq >= 0 && idSeq <= maxSeq

    if (!isValidWorkerId || !isValidSequence) {
      return false;
    }

    const timestamp = Number((idInt >> BigInt(bits + seq)) + BigInt(epoch))

    if (timestamp < 0 || timestamp > Date.now()) {
      return false;
    }

    return true;
  }
  
  function created_at(id: string): number {
    const timestamp = (BigInt(id) >> BigInt(bits + seq)) + BigInt(epoch)

    return Number(timestamp);
  }

  return { generate, isValid, created_at, worker, epoch, bits, seq };
}

const snowflake = Snowflake({})

export function uuid(ts?: number) {
  return snowflake.generate(ts)
}

export function is_valid(id: string): boolean {
  return snowflake.isValid(id);
}

export function created_at(id: string): number {
  return snowflake.created_at(id)
}

export default snowflake;