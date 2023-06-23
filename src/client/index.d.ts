
/**
 * Client
**/

import * as runtime from './runtime/library';
type UnwrapPromise<P extends any> = P extends Promise<infer R> ? R : P
type UnwrapTuple<Tuple extends readonly unknown[]> = {
  [K in keyof Tuple]: K extends `${number}` ? Tuple[K] extends Prisma.PrismaPromise<infer X> ? X : UnwrapPromise<Tuple[K]> : UnwrapPromise<Tuple[K]>
};

export type PrismaPromise<T> = runtime.Types.Public.PrismaPromise<T>


/**
 * Model Guild
 * 
 */
export type Guild = {
  id: string
  created_at: Date
  updated_at: Date
}

/**
 * Model Art
 * 
 */
export type Art = {
  name: string
  key: string
  type: ArtType
  role: string | null
  guild_id: string
  embed_title: string | null
  embed_description: string | null
  embed_url: string | null
  created_at: Date
  updated_at: Date
}

/**
 * Model Attack
 * 
 */
export type Attack = {
  name: string
  key: string
  art_key: string
  guild_id: string
  roles: string[]
  required_roles: number
  required_exp: number
  damage: number
  stamina: number
  embed_title: string | null
  embed_description: string | null
  embed_url: string | null
  fields_key: string | null
  created_at: Date
  updated_at: Date
}

/**
 * Model Varialble
 * 
 */
export type Varialble = {
  guild_id: string
  name: string
  text: string
  visibleCaseIfNotAuthorizerMember: boolean
  required_roles: number
  roles: string[]
  created_at: Date
  updated_at: Date
}


/**
 * Enums
 */

export const ArtType: {
  RESPIRATION: 'RESPIRATION',
  KEKKIJUTSU: 'KEKKIJUTSU'
};

export type ArtType = (typeof ArtType)[keyof typeof ArtType]


/**
 * ##  Prisma Client ʲˢ
 * 
 * Type-safe database client for TypeScript & Node.js
 * @example
 * ```
 * const prisma = new PrismaClient()
 * // Fetch zero or more Guilds
 * const guilds = await prisma.guild.findMany()
 * ```
 *
 * 
 * Read more in our [docs](https://www.prisma.io/docs/reference/tools-and-interfaces/prisma-client).
 */
export class PrismaClient<
  T extends Prisma.PrismaClientOptions = Prisma.PrismaClientOptions,
  U = 'log' extends keyof T ? T['log'] extends Array<Prisma.LogLevel | Prisma.LogDefinition> ? Prisma.GetEvents<T['log']> : never : never,
  GlobalReject extends Prisma.RejectOnNotFound | Prisma.RejectPerOperation | false | undefined = 'rejectOnNotFound' extends keyof T
    ? T['rejectOnNotFound']
    : false
      > {
    /**
   * ##  Prisma Client ʲˢ
   * 
   * Type-safe database client for TypeScript & Node.js
   * @example
   * ```
   * const prisma = new PrismaClient()
   * // Fetch zero or more Guilds
   * const guilds = await prisma.guild.findMany()
   * ```
   *
   * 
   * Read more in our [docs](https://www.prisma.io/docs/reference/tools-and-interfaces/prisma-client).
   */

  constructor(optionsArg ?: Prisma.Subset<T, Prisma.PrismaClientOptions>);
  $on<V extends (U | 'beforeExit')>(eventType: V, callback: (event: V extends 'query' ? Prisma.QueryEvent : V extends 'beforeExit' ? () => Promise<void> : Prisma.LogEvent) => void): void;

  /**
   * Connect with the database
   */
  $connect(): Promise<void>;

  /**
   * Disconnect from the database
   */
  $disconnect(): Promise<void>;

  /**
   * Add a middleware
   */
  $use(cb: Prisma.Middleware): void

/**
   * Executes a prepared raw query and returns the number of affected rows.
   * @example
   * ```
   * const result = await prisma.$executeRaw`UPDATE User SET cool = ${true} WHERE email = ${'user@email.com'};`
   * ```
   * 
   * Read more in our [docs](https://www.prisma.io/docs/reference/tools-and-interfaces/prisma-client/raw-database-access).
   */
  $executeRaw<T = unknown>(query: TemplateStringsArray | Prisma.Sql, ...values: any[]): Prisma.PrismaPromise<number>;

  /**
   * Executes a raw query and returns the number of affected rows.
   * Susceptible to SQL injections, see documentation.
   * @example
   * ```
   * const result = await prisma.$executeRawUnsafe('UPDATE User SET cool = $1 WHERE email = $2 ;', true, 'user@email.com')
   * ```
   * 
   * Read more in our [docs](https://www.prisma.io/docs/reference/tools-and-interfaces/prisma-client/raw-database-access).
   */
  $executeRawUnsafe<T = unknown>(query: string, ...values: any[]): Prisma.PrismaPromise<number>;

  /**
   * Performs a prepared raw query and returns the `SELECT` data.
   * @example
   * ```
   * const result = await prisma.$queryRaw`SELECT * FROM User WHERE id = ${1} OR email = ${'user@email.com'};`
   * ```
   * 
   * Read more in our [docs](https://www.prisma.io/docs/reference/tools-and-interfaces/prisma-client/raw-database-access).
   */
  $queryRaw<T = unknown>(query: TemplateStringsArray | Prisma.Sql, ...values: any[]): Prisma.PrismaPromise<T>;

  /**
   * Performs a raw query and returns the `SELECT` data.
   * Susceptible to SQL injections, see documentation.
   * @example
   * ```
   * const result = await prisma.$queryRawUnsafe('SELECT * FROM User WHERE id = $1 OR email = $2;', 1, 'user@email.com')
   * ```
   * 
   * Read more in our [docs](https://www.prisma.io/docs/reference/tools-and-interfaces/prisma-client/raw-database-access).
   */
  $queryRawUnsafe<T = unknown>(query: string, ...values: any[]): Prisma.PrismaPromise<T>;

  /**
   * Allows the running of a sequence of read/write operations that are guaranteed to either succeed or fail as a whole.
   * @example
   * ```
   * const [george, bob, alice] = await prisma.$transaction([
   *   prisma.user.create({ data: { name: 'George' } }),
   *   prisma.user.create({ data: { name: 'Bob' } }),
   *   prisma.user.create({ data: { name: 'Alice' } }),
   * ])
   * ```
   * 
   * Read more in our [docs](https://www.prisma.io/docs/concepts/components/prisma-client/transactions).
   */
  $transaction<P extends Prisma.PrismaPromise<any>[]>(arg: [...P], options?: { isolationLevel?: Prisma.TransactionIsolationLevel }): Promise<UnwrapTuple<P>>

  $transaction<R>(fn: (prisma: Omit<this, "$connect" | "$disconnect" | "$on" | "$transaction" | "$use">) => Promise<R>, options?: { maxWait?: number, timeout?: number, isolationLevel?: Prisma.TransactionIsolationLevel }): Promise<R>

      /**
   * `prisma.guild`: Exposes CRUD operations for the **Guild** model.
    * Example usage:
    * ```ts
    * // Fetch zero or more Guilds
    * const guilds = await prisma.guild.findMany()
    * ```
    */
  get guild(): Prisma.GuildDelegate<GlobalReject>;

  /**
   * `prisma.art`: Exposes CRUD operations for the **Art** model.
    * Example usage:
    * ```ts
    * // Fetch zero or more Arts
    * const arts = await prisma.art.findMany()
    * ```
    */
  get art(): Prisma.ArtDelegate<GlobalReject>;

  /**
   * `prisma.attack`: Exposes CRUD operations for the **Attack** model.
    * Example usage:
    * ```ts
    * // Fetch zero or more Attacks
    * const attacks = await prisma.attack.findMany()
    * ```
    */
  get attack(): Prisma.AttackDelegate<GlobalReject>;

  /**
   * `prisma.varialble`: Exposes CRUD operations for the **Varialble** model.
    * Example usage:
    * ```ts
    * // Fetch zero or more Varialbles
    * const varialbles = await prisma.varialble.findMany()
    * ```
    */
  get varialble(): Prisma.VarialbleDelegate<GlobalReject>;
}

export namespace Prisma {
  export import DMMF = runtime.DMMF

  export type PrismaPromise<T> = runtime.Types.Public.PrismaPromise<T>

  /**
   * Prisma Errors
   */
  export import PrismaClientKnownRequestError = runtime.PrismaClientKnownRequestError
  export import PrismaClientUnknownRequestError = runtime.PrismaClientUnknownRequestError
  export import PrismaClientRustPanicError = runtime.PrismaClientRustPanicError
  export import PrismaClientInitializationError = runtime.PrismaClientInitializationError
  export import PrismaClientValidationError = runtime.PrismaClientValidationError
  export import NotFoundError = runtime.NotFoundError

  /**
   * Re-export of sql-template-tag
   */
  export import sql = runtime.sqltag
  export import empty = runtime.empty
  export import join = runtime.join
  export import raw = runtime.raw
  export import Sql = runtime.Sql

  /**
   * Decimal.js
   */
  export import Decimal = runtime.Decimal

  export type DecimalJsLike = runtime.DecimalJsLike

  /**
   * Metrics 
   */
  export type Metrics = runtime.Metrics
  export type Metric<T> = runtime.Metric<T>
  export type MetricHistogram = runtime.MetricHistogram
  export type MetricHistogramBucket = runtime.MetricHistogramBucket


  /**
   * Prisma Client JS version: 4.15.0
   * Query Engine version: 8fbc245156db7124f997f4cecdd8d1219e360944
   */
  export type PrismaVersion = {
    client: string
  }

  export const prismaVersion: PrismaVersion 

  /**
   * Utility Types
   */

  /**
   * From https://github.com/sindresorhus/type-fest/
   * Matches a JSON object.
   * This type can be useful to enforce some input to be JSON-compatible or as a super-type to be extended from. 
   */
  export type JsonObject = {[Key in string]?: JsonValue}

  /**
   * From https://github.com/sindresorhus/type-fest/
   * Matches a JSON array.
   */
  export interface JsonArray extends Array<JsonValue> {}

  /**
   * From https://github.com/sindresorhus/type-fest/
   * Matches any valid JSON value.
   */
  export type JsonValue = string | number | boolean | JsonObject | JsonArray | null

  /**
   * Matches a JSON object.
   * Unlike `JsonObject`, this type allows undefined and read-only properties.
   */
  export type InputJsonObject = {readonly [Key in string]?: InputJsonValue | null}

  /**
   * Matches a JSON array.
   * Unlike `JsonArray`, readonly arrays are assignable to this type.
   */
  export interface InputJsonArray extends ReadonlyArray<InputJsonValue | null> {}

  /**
   * Matches any valid value that can be used as an input for operations like
   * create and update as the value of a JSON field. Unlike `JsonValue`, this
   * type allows read-only arrays and read-only object properties and disallows
   * `null` at the top level.
   *
   * `null` cannot be used as the value of a JSON field because its meaning
   * would be ambiguous. Use `Prisma.JsonNull` to store the JSON null value or
   * `Prisma.DbNull` to clear the JSON value and set the field to the database
   * NULL value instead.
   *
   * @see https://www.prisma.io/docs/concepts/components/prisma-client/working-with-fields/working-with-json-fields#filtering-by-null-values
   */
  export type InputJsonValue = string | number | boolean | InputJsonObject | InputJsonArray

  /**
   * Types of the values used to represent different kinds of `null` values when working with JSON fields.
   * 
   * @see https://www.prisma.io/docs/concepts/components/prisma-client/working-with-fields/working-with-json-fields#filtering-on-a-json-field
   */
  namespace NullTypes {
    /**
    * Type of `Prisma.DbNull`.
    * 
    * You cannot use other instances of this class. Please use the `Prisma.DbNull` value.
    * 
    * @see https://www.prisma.io/docs/concepts/components/prisma-client/working-with-fields/working-with-json-fields#filtering-on-a-json-field
    */
    class DbNull {
      private DbNull: never
      private constructor()
    }

    /**
    * Type of `Prisma.JsonNull`.
    * 
    * You cannot use other instances of this class. Please use the `Prisma.JsonNull` value.
    * 
    * @see https://www.prisma.io/docs/concepts/components/prisma-client/working-with-fields/working-with-json-fields#filtering-on-a-json-field
    */
    class JsonNull {
      private JsonNull: never
      private constructor()
    }

    /**
    * Type of `Prisma.AnyNull`.
    * 
    * You cannot use other instances of this class. Please use the `Prisma.AnyNull` value.
    * 
    * @see https://www.prisma.io/docs/concepts/components/prisma-client/working-with-fields/working-with-json-fields#filtering-on-a-json-field
    */
    class AnyNull {
      private AnyNull: never
      private constructor()
    }
  }

  /**
   * Helper for filtering JSON entries that have `null` on the database (empty on the db)
   * 
   * @see https://www.prisma.io/docs/concepts/components/prisma-client/working-with-fields/working-with-json-fields#filtering-on-a-json-field
   */
  export const DbNull: NullTypes.DbNull

  /**
   * Helper for filtering JSON entries that have JSON `null` values (not empty on the db)
   * 
   * @see https://www.prisma.io/docs/concepts/components/prisma-client/working-with-fields/working-with-json-fields#filtering-on-a-json-field
   */
  export const JsonNull: NullTypes.JsonNull

  /**
   * Helper for filtering JSON entries that are `Prisma.DbNull` or `Prisma.JsonNull`
   * 
   * @see https://www.prisma.io/docs/concepts/components/prisma-client/working-with-fields/working-with-json-fields#filtering-on-a-json-field
   */
  export const AnyNull: NullTypes.AnyNull

  type SelectAndInclude = {
    select: any
    include: any
  }
  type HasSelect = {
    select: any
  }
  type HasInclude = {
    include: any
  }
  type CheckSelect<T, S, U> = T extends SelectAndInclude
    ? 'Please either choose `select` or `include`'
    : T extends HasSelect
    ? U
    : T extends HasInclude
    ? U
    : S

  /**
   * Get the type of the value, that the Promise holds.
   */
  export type PromiseType<T extends PromiseLike<any>> = T extends PromiseLike<infer U> ? U : T;

  /**
   * Get the return type of a function which returns a Promise.
   */
  export type PromiseReturnType<T extends (...args: any) => Promise<any>> = PromiseType<ReturnType<T>>

  /**
   * From T, pick a set of properties whose keys are in the union K
   */
  type Prisma__Pick<T, K extends keyof T> = {
      [P in K]: T[P];
  };


  export type Enumerable<T> = T | Array<T>;

  export type RequiredKeys<T> = {
    [K in keyof T]-?: {} extends Prisma__Pick<T, K> ? never : K
  }[keyof T]

  export type TruthyKeys<T> = keyof {
    [K in keyof T as T[K] extends false | undefined | null ? never : K]: K
  }

  export type TrueKeys<T> = TruthyKeys<Prisma__Pick<T, RequiredKeys<T>>>

  /**
   * Subset
   * @desc From `T` pick properties that exist in `U`. Simple version of Intersection
   */
  export type Subset<T, U> = {
    [key in keyof T]: key extends keyof U ? T[key] : never;
  };

  /**
   * SelectSubset
   * @desc From `T` pick properties that exist in `U`. Simple version of Intersection.
   * Additionally, it validates, if both select and include are present. If the case, it errors.
   */
  export type SelectSubset<T, U> = {
    [key in keyof T]: key extends keyof U ? T[key] : never
  } &
    (T extends SelectAndInclude
      ? 'Please either choose `select` or `include`.'
      : {})

  /**
   * Subset + Intersection
   * @desc From `T` pick properties that exist in `U` and intersect `K`
   */
  export type SubsetIntersection<T, U, K> = {
    [key in keyof T]: key extends keyof U ? T[key] : never
  } &
    K

  type Without<T, U> = { [P in Exclude<keyof T, keyof U>]?: never };

  /**
   * XOR is needed to have a real mutually exclusive union type
   * https://stackoverflow.com/questions/42123407/does-typescript-support-mutually-exclusive-types
   */
  type XOR<T, U> =
    T extends object ?
    U extends object ?
      (Without<T, U> & U) | (Without<U, T> & T)
    : U : T


  /**
   * Is T a Record?
   */
  type IsObject<T extends any> = T extends Array<any>
  ? False
  : T extends Date
  ? False
  : T extends Uint8Array
  ? False
  : T extends BigInt
  ? False
  : T extends object
  ? True
  : False


  /**
   * If it's T[], return T
   */
  export type UnEnumerate<T extends unknown> = T extends Array<infer U> ? U : T

  /**
   * From ts-toolbelt
   */

  type __Either<O extends object, K extends Key> = Omit<O, K> &
    {
      // Merge all but K
      [P in K]: Prisma__Pick<O, P & keyof O> // With K possibilities
    }[K]

  type EitherStrict<O extends object, K extends Key> = Strict<__Either<O, K>>

  type EitherLoose<O extends object, K extends Key> = ComputeRaw<__Either<O, K>>

  type _Either<
    O extends object,
    K extends Key,
    strict extends Boolean
  > = {
    1: EitherStrict<O, K>
    0: EitherLoose<O, K>
  }[strict]

  type Either<
    O extends object,
    K extends Key,
    strict extends Boolean = 1
  > = O extends unknown ? _Either<O, K, strict> : never

  export type Union = any

  type PatchUndefined<O extends object, O1 extends object> = {
    [K in keyof O]: O[K] extends undefined ? At<O1, K> : O[K]
  } & {}

  /** Helper Types for "Merge" **/
  export type IntersectOf<U extends Union> = (
    U extends unknown ? (k: U) => void : never
  ) extends (k: infer I) => void
    ? I
    : never

  export type Overwrite<O extends object, O1 extends object> = {
      [K in keyof O]: K extends keyof O1 ? O1[K] : O[K];
  } & {};

  type _Merge<U extends object> = IntersectOf<Overwrite<U, {
      [K in keyof U]-?: At<U, K>;
  }>>;

  type Key = string | number | symbol;
  type AtBasic<O extends object, K extends Key> = K extends keyof O ? O[K] : never;
  type AtStrict<O extends object, K extends Key> = O[K & keyof O];
  type AtLoose<O extends object, K extends Key> = O extends unknown ? AtStrict<O, K> : never;
  export type At<O extends object, K extends Key, strict extends Boolean = 1> = {
      1: AtStrict<O, K>;
      0: AtLoose<O, K>;
  }[strict];

  export type ComputeRaw<A extends any> = A extends Function ? A : {
    [K in keyof A]: A[K];
  } & {};

  export type OptionalFlat<O> = {
    [K in keyof O]?: O[K];
  } & {};

  type _Record<K extends keyof any, T> = {
    [P in K]: T;
  };

  // cause typescript not to expand types and preserve names
  type NoExpand<T> = T extends unknown ? T : never;

  // this type assumes the passed object is entirely optional
  type AtLeast<O extends object, K extends string> = NoExpand<
    O extends unknown
    ? | (K extends keyof O ? { [P in K]: O[P] } & O : O)
      | {[P in keyof O as P extends K ? K : never]-?: O[P]} & O
    : never>;

  type _Strict<U, _U = U> = U extends unknown ? U & OptionalFlat<_Record<Exclude<Keys<_U>, keyof U>, never>> : never;

  export type Strict<U extends object> = ComputeRaw<_Strict<U>>;
  /** End Helper Types for "Merge" **/

  export type Merge<U extends object> = ComputeRaw<_Merge<Strict<U>>>;

  /**
  A [[Boolean]]
  */
  export type Boolean = True | False

  // /**
  // 1
  // */
  export type True = 1

  /**
  0
  */
  export type False = 0

  export type Not<B extends Boolean> = {
    0: 1
    1: 0
  }[B]

  export type Extends<A1 extends any, A2 extends any> = [A1] extends [never]
    ? 0 // anything `never` is false
    : A1 extends A2
    ? 1
    : 0

  export type Has<U extends Union, U1 extends Union> = Not<
    Extends<Exclude<U1, U>, U1>
  >

  export type Or<B1 extends Boolean, B2 extends Boolean> = {
    0: {
      0: 0
      1: 1
    }
    1: {
      0: 1
      1: 1
    }
  }[B1][B2]

  export type Keys<U extends Union> = U extends unknown ? keyof U : never

  type Cast<A, B> = A extends B ? A : B;

  export const type: unique symbol;

  export function validator<V>(): <S>(select: runtime.Types.Utils.LegacyExact<S, V>) => S;

  /**
   * Used by group by
   */

  export type GetScalarType<T, O> = O extends object ? {
    [P in keyof T]: P extends keyof O
      ? O[P]
      : never
  } : never

  type FieldPaths<
    T,
    U = Omit<T, '_avg' | '_sum' | '_count' | '_min' | '_max'>
  > = IsObject<T> extends True ? U : T

  type GetHavingFields<T> = {
    [K in keyof T]: Or<
      Or<Extends<'OR', K>, Extends<'AND', K>>,
      Extends<'NOT', K>
    > extends True
      ? // infer is only needed to not hit TS limit
        // based on the brilliant idea of Pierre-Antoine Mills
        // https://github.com/microsoft/TypeScript/issues/30188#issuecomment-478938437
        T[K] extends infer TK
        ? GetHavingFields<UnEnumerate<TK> extends object ? Merge<UnEnumerate<TK>> : never>
        : never
      : {} extends FieldPaths<T[K]>
      ? never
      : K
  }[keyof T]

  /**
   * Convert tuple to union
   */
  type _TupleToUnion<T> = T extends (infer E)[] ? E : never
  type TupleToUnion<K extends readonly any[]> = _TupleToUnion<K>
  type MaybeTupleToUnion<T> = T extends any[] ? TupleToUnion<T> : T

  /**
   * Like `Pick`, but with an array
   */
  type PickArray<T, K extends Array<keyof T>> = Prisma__Pick<T, TupleToUnion<K>>

  /**
   * Exclude all keys with underscores
   */
  type ExcludeUnderscoreKeys<T extends string> = T extends `_${string}` ? never : T


  export type FieldRef<Model, FieldType> = runtime.FieldRef<Model, FieldType>

  type FieldRefInputType<Model, FieldType> = Model extends never ? never : FieldRef<Model, FieldType>


  export const ModelName: {
    Guild: 'Guild',
    Art: 'Art',
    Attack: 'Attack',
    Varialble: 'Varialble'
  };

  export type ModelName = (typeof ModelName)[keyof typeof ModelName]


  export type Datasources = {
    db?: Datasource
  }

  export type DefaultPrismaClient = PrismaClient
  export type RejectOnNotFound = boolean | ((error: Error) => Error)
  export type RejectPerModel = { [P in ModelName]?: RejectOnNotFound }
  export type RejectPerOperation =  { [P in "findUnique" | "findFirst"]?: RejectPerModel | RejectOnNotFound } 
  type IsReject<T> = T extends true ? True : T extends (err: Error) => Error ? True : False
  export type HasReject<
    GlobalRejectSettings extends Prisma.PrismaClientOptions['rejectOnNotFound'],
    LocalRejectSettings,
    Action extends PrismaAction,
    Model extends ModelName
  > = LocalRejectSettings extends RejectOnNotFound
    ? IsReject<LocalRejectSettings>
    : GlobalRejectSettings extends RejectPerOperation
    ? Action extends keyof GlobalRejectSettings
      ? GlobalRejectSettings[Action] extends RejectOnNotFound
        ? IsReject<GlobalRejectSettings[Action]>
        : GlobalRejectSettings[Action] extends RejectPerModel
        ? Model extends keyof GlobalRejectSettings[Action]
          ? IsReject<GlobalRejectSettings[Action][Model]>
          : False
        : False
      : False
    : IsReject<GlobalRejectSettings>
  export type ErrorFormat = 'pretty' | 'colorless' | 'minimal'

  export interface PrismaClientOptions {
    /**
     * Configure findUnique/findFirst to throw an error if the query returns null. 
     * @deprecated since 4.0.0. Use `findUniqueOrThrow`/`findFirstOrThrow` methods instead.
     * @example
     * ```
     * // Reject on both findUnique/findFirst
     * rejectOnNotFound: true
     * // Reject only on findFirst with a custom error
     * rejectOnNotFound: { findFirst: (err) => new Error("Custom Error")}
     * // Reject on user.findUnique with a custom error
     * rejectOnNotFound: { findUnique: {User: (err) => new Error("User not found")}}
     * ```
     */
    rejectOnNotFound?: RejectOnNotFound | RejectPerOperation
    /**
     * Overwrites the datasource url from your schema.prisma file
     */
    datasources?: Datasources

    /**
     * @default "colorless"
     */
    errorFormat?: ErrorFormat

    /**
     * @example
     * ```
     * // Defaults to stdout
     * log: ['query', 'info', 'warn', 'error']
     * 
     * // Emit as events
     * log: [
     *  { emit: 'stdout', level: 'query' },
     *  { emit: 'stdout', level: 'info' },
     *  { emit: 'stdout', level: 'warn' }
     *  { emit: 'stdout', level: 'error' }
     * ]
     * ```
     * Read more in our [docs](https://www.prisma.io/docs/reference/tools-and-interfaces/prisma-client/logging#the-log-option).
     */
    log?: Array<LogLevel | LogDefinition>
  }

  /* Types for Logging */
  export type LogLevel = 'info' | 'query' | 'warn' | 'error'
  export type LogDefinition = {
    level: LogLevel
    emit: 'stdout' | 'event'
  }

  export type GetLogType<T extends LogLevel | LogDefinition> = T extends LogDefinition ? T['emit'] extends 'event' ? T['level'] : never : never
  export type GetEvents<T extends any> = T extends Array<LogLevel | LogDefinition> ?
    GetLogType<T[0]> | GetLogType<T[1]> | GetLogType<T[2]> | GetLogType<T[3]>
    : never

  export type QueryEvent = {
    timestamp: Date
    query: string
    params: string
    duration: number
    target: string
  }

  export type LogEvent = {
    timestamp: Date
    message: string
    target: string
  }
  /* End Types for Logging */


  export type PrismaAction =
    | 'findUnique'
    | 'findMany'
    | 'findFirst'
    | 'create'
    | 'createMany'
    | 'update'
    | 'updateMany'
    | 'upsert'
    | 'delete'
    | 'deleteMany'
    | 'executeRaw'
    | 'queryRaw'
    | 'aggregate'
    | 'count'
    | 'runCommandRaw'
    | 'findRaw'

  /**
   * These options are being passed into the middleware as "params"
   */
  export type MiddlewareParams = {
    model?: ModelName
    action: PrismaAction
    args: any
    dataPath: string[]
    runInTransaction: boolean
  }

  /**
   * The `T` type makes sure, that the `return proceed` is not forgotten in the middleware implementation
   */
  export type Middleware<T = any> = (
    params: MiddlewareParams,
    next: (params: MiddlewareParams) => Promise<T>,
  ) => Promise<T>

  // tested in getLogLevel.test.ts
  export function getLogLevel(log: Array<LogLevel | LogDefinition>): LogLevel | undefined;

  /**
   * `PrismaClient` proxy available in interactive transactions.
   */
  export type TransactionClient = Omit<Prisma.DefaultPrismaClient, '$connect' | '$disconnect' | '$on' | '$transaction' | '$use'>

  export type Datasource = {
    url?: string
  }

  /**
   * Count Types
   */


  /**
   * Count Type GuildCountOutputType
   */


  export type GuildCountOutputType = {
    arts: number
    vars: number
  }

  export type GuildCountOutputTypeSelect = {
    arts?: boolean
    vars?: boolean
  }

  export type GuildCountOutputTypeGetPayload<S extends boolean | null | undefined | GuildCountOutputTypeArgs> =
    S extends { select: any, include: any } ? 'Please either choose `select` or `include`' :
    S extends true ? GuildCountOutputType :
    S extends undefined ? never :
    S extends { include: any } & (GuildCountOutputTypeArgs)
    ? GuildCountOutputType 
    : S extends { select: any } & (GuildCountOutputTypeArgs)
      ? {
    [P in TruthyKeys<S['select']>]:
    P extends keyof GuildCountOutputType ? GuildCountOutputType[P] : never
  } 
      : GuildCountOutputType




  // Custom InputTypes

  /**
   * GuildCountOutputType without action
   */
  export type GuildCountOutputTypeArgs = {
    /**
     * Select specific fields to fetch from the GuildCountOutputType
     */
    select?: GuildCountOutputTypeSelect | null
  }



  /**
   * Count Type ArtCountOutputType
   */


  export type ArtCountOutputType = {
    attacks: number
  }

  export type ArtCountOutputTypeSelect = {
    attacks?: boolean
  }

  export type ArtCountOutputTypeGetPayload<S extends boolean | null | undefined | ArtCountOutputTypeArgs> =
    S extends { select: any, include: any } ? 'Please either choose `select` or `include`' :
    S extends true ? ArtCountOutputType :
    S extends undefined ? never :
    S extends { include: any } & (ArtCountOutputTypeArgs)
    ? ArtCountOutputType 
    : S extends { select: any } & (ArtCountOutputTypeArgs)
      ? {
    [P in TruthyKeys<S['select']>]:
    P extends keyof ArtCountOutputType ? ArtCountOutputType[P] : never
  } 
      : ArtCountOutputType




  // Custom InputTypes

  /**
   * ArtCountOutputType without action
   */
  export type ArtCountOutputTypeArgs = {
    /**
     * Select specific fields to fetch from the ArtCountOutputType
     */
    select?: ArtCountOutputTypeSelect | null
  }



  /**
   * Models
   */

  /**
   * Model Guild
   */


  export type AggregateGuild = {
    _count: GuildCountAggregateOutputType | null
    _min: GuildMinAggregateOutputType | null
    _max: GuildMaxAggregateOutputType | null
  }

  export type GuildMinAggregateOutputType = {
    id: string | null
    created_at: Date | null
    updated_at: Date | null
  }

  export type GuildMaxAggregateOutputType = {
    id: string | null
    created_at: Date | null
    updated_at: Date | null
  }

  export type GuildCountAggregateOutputType = {
    id: number
    created_at: number
    updated_at: number
    _all: number
  }


  export type GuildMinAggregateInputType = {
    id?: true
    created_at?: true
    updated_at?: true
  }

  export type GuildMaxAggregateInputType = {
    id?: true
    created_at?: true
    updated_at?: true
  }

  export type GuildCountAggregateInputType = {
    id?: true
    created_at?: true
    updated_at?: true
    _all?: true
  }

  export type GuildAggregateArgs = {
    /**
     * Filter which Guild to aggregate.
     */
    where?: GuildWhereInput
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/sorting Sorting Docs}
     * 
     * Determine the order of Guilds to fetch.
     */
    orderBy?: Enumerable<GuildOrderByWithRelationInput>
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/pagination#cursor-based-pagination Cursor Docs}
     * 
     * Sets the start position
     */
    cursor?: GuildWhereUniqueInput
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/pagination Pagination Docs}
     * 
     * Take `±n` Guilds from the position of the cursor.
     */
    take?: number
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/pagination Pagination Docs}
     * 
     * Skip the first `n` Guilds.
     */
    skip?: number
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/aggregations Aggregation Docs}
     * 
     * Count returned Guilds
    **/
    _count?: true | GuildCountAggregateInputType
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/aggregations Aggregation Docs}
     * 
     * Select which fields to find the minimum value
    **/
    _min?: GuildMinAggregateInputType
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/aggregations Aggregation Docs}
     * 
     * Select which fields to find the maximum value
    **/
    _max?: GuildMaxAggregateInputType
  }

  export type GetGuildAggregateType<T extends GuildAggregateArgs> = {
        [P in keyof T & keyof AggregateGuild]: P extends '_count' | 'count'
      ? T[P] extends true
        ? number
        : GetScalarType<T[P], AggregateGuild[P]>
      : GetScalarType<T[P], AggregateGuild[P]>
  }




  export type GuildGroupByArgs = {
    where?: GuildWhereInput
    orderBy?: Enumerable<GuildOrderByWithAggregationInput>
    by: GuildScalarFieldEnum[]
    having?: GuildScalarWhereWithAggregatesInput
    take?: number
    skip?: number
    _count?: GuildCountAggregateInputType | true
    _min?: GuildMinAggregateInputType
    _max?: GuildMaxAggregateInputType
  }


  export type GuildGroupByOutputType = {
    id: string
    created_at: Date
    updated_at: Date
    _count: GuildCountAggregateOutputType | null
    _min: GuildMinAggregateOutputType | null
    _max: GuildMaxAggregateOutputType | null
  }

  type GetGuildGroupByPayload<T extends GuildGroupByArgs> = Prisma.PrismaPromise<
    Array<
      PickArray<GuildGroupByOutputType, T['by']> &
        {
          [P in ((keyof T) & (keyof GuildGroupByOutputType))]: P extends '_count'
            ? T[P] extends boolean
              ? number
              : GetScalarType<T[P], GuildGroupByOutputType[P]>
            : GetScalarType<T[P], GuildGroupByOutputType[P]>
        }
      >
    >


  export type GuildSelect = {
    id?: boolean
    created_at?: boolean
    updated_at?: boolean
    arts?: boolean | Guild$artsArgs
    vars?: boolean | Guild$varsArgs
    _count?: boolean | GuildCountOutputTypeArgs
  }


  export type GuildInclude = {
    arts?: boolean | Guild$artsArgs
    vars?: boolean | Guild$varsArgs
    _count?: boolean | GuildCountOutputTypeArgs
  }

  export type GuildGetPayload<S extends boolean | null | undefined | GuildArgs> =
    S extends { select: any, include: any } ? 'Please either choose `select` or `include`' :
    S extends true ? Guild :
    S extends undefined ? never :
    S extends { include: any } & (GuildArgs | GuildFindManyArgs)
    ? Guild  & {
    [P in TruthyKeys<S['include']>]:
        P extends 'arts' ? Array < ArtGetPayload<S['include'][P]>>  :
        P extends 'vars' ? Array < VarialbleGetPayload<S['include'][P]>>  :
        P extends '_count' ? GuildCountOutputTypeGetPayload<S['include'][P]> :  never
  } 
    : S extends { select: any } & (GuildArgs | GuildFindManyArgs)
      ? {
    [P in TruthyKeys<S['select']>]:
        P extends 'arts' ? Array < ArtGetPayload<S['select'][P]>>  :
        P extends 'vars' ? Array < VarialbleGetPayload<S['select'][P]>>  :
        P extends '_count' ? GuildCountOutputTypeGetPayload<S['select'][P]> :  P extends keyof Guild ? Guild[P] : never
  } 
      : Guild


  type GuildCountArgs = 
    Omit<GuildFindManyArgs, 'select' | 'include'> & {
      select?: GuildCountAggregateInputType | true
    }

  export interface GuildDelegate<GlobalRejectSettings extends Prisma.RejectOnNotFound | Prisma.RejectPerOperation | false | undefined> {

    /**
     * Find zero or one Guild that matches the filter.
     * @param {GuildFindUniqueArgs} args - Arguments to find a Guild
     * @example
     * // Get one Guild
     * const guild = await prisma.guild.findUnique({
     *   where: {
     *     // ... provide filter here
     *   }
     * })
    **/
    findUnique<T extends GuildFindUniqueArgs,  LocalRejectSettings = T["rejectOnNotFound"] extends RejectOnNotFound ? T['rejectOnNotFound'] : undefined>(
      args: SelectSubset<T, GuildFindUniqueArgs>
    ): HasReject<GlobalRejectSettings, LocalRejectSettings, 'findUnique', 'Guild'> extends True ? Prisma__GuildClient<GuildGetPayload<T>> : Prisma__GuildClient<GuildGetPayload<T> | null, null>

    /**
     * Find one Guild that matches the filter or throw an error  with `error.code='P2025'` 
     *     if no matches were found.
     * @param {GuildFindUniqueOrThrowArgs} args - Arguments to find a Guild
     * @example
     * // Get one Guild
     * const guild = await prisma.guild.findUniqueOrThrow({
     *   where: {
     *     // ... provide filter here
     *   }
     * })
    **/
    findUniqueOrThrow<T extends GuildFindUniqueOrThrowArgs>(
      args?: SelectSubset<T, GuildFindUniqueOrThrowArgs>
    ): Prisma__GuildClient<GuildGetPayload<T>>

    /**
     * Find the first Guild that matches the filter.
     * Note, that providing `undefined` is treated as the value not being there.
     * Read more here: https://pris.ly/d/null-undefined
     * @param {GuildFindFirstArgs} args - Arguments to find a Guild
     * @example
     * // Get one Guild
     * const guild = await prisma.guild.findFirst({
     *   where: {
     *     // ... provide filter here
     *   }
     * })
    **/
    findFirst<T extends GuildFindFirstArgs,  LocalRejectSettings = T["rejectOnNotFound"] extends RejectOnNotFound ? T['rejectOnNotFound'] : undefined>(
      args?: SelectSubset<T, GuildFindFirstArgs>
    ): HasReject<GlobalRejectSettings, LocalRejectSettings, 'findFirst', 'Guild'> extends True ? Prisma__GuildClient<GuildGetPayload<T>> : Prisma__GuildClient<GuildGetPayload<T> | null, null>

    /**
     * Find the first Guild that matches the filter or
     * throw `NotFoundError` if no matches were found.
     * Note, that providing `undefined` is treated as the value not being there.
     * Read more here: https://pris.ly/d/null-undefined
     * @param {GuildFindFirstOrThrowArgs} args - Arguments to find a Guild
     * @example
     * // Get one Guild
     * const guild = await prisma.guild.findFirstOrThrow({
     *   where: {
     *     // ... provide filter here
     *   }
     * })
    **/
    findFirstOrThrow<T extends GuildFindFirstOrThrowArgs>(
      args?: SelectSubset<T, GuildFindFirstOrThrowArgs>
    ): Prisma__GuildClient<GuildGetPayload<T>>

    /**
     * Find zero or more Guilds that matches the filter.
     * Note, that providing `undefined` is treated as the value not being there.
     * Read more here: https://pris.ly/d/null-undefined
     * @param {GuildFindManyArgs=} args - Arguments to filter and select certain fields only.
     * @example
     * // Get all Guilds
     * const guilds = await prisma.guild.findMany()
     * 
     * // Get first 10 Guilds
     * const guilds = await prisma.guild.findMany({ take: 10 })
     * 
     * // Only select the `id`
     * const guildWithIdOnly = await prisma.guild.findMany({ select: { id: true } })
     * 
    **/
    findMany<T extends GuildFindManyArgs>(
      args?: SelectSubset<T, GuildFindManyArgs>
    ): Prisma.PrismaPromise<Array<GuildGetPayload<T>>>

    /**
     * Create a Guild.
     * @param {GuildCreateArgs} args - Arguments to create a Guild.
     * @example
     * // Create one Guild
     * const Guild = await prisma.guild.create({
     *   data: {
     *     // ... data to create a Guild
     *   }
     * })
     * 
    **/
    create<T extends GuildCreateArgs>(
      args: SelectSubset<T, GuildCreateArgs>
    ): Prisma__GuildClient<GuildGetPayload<T>>

    /**
     * Create many Guilds.
     *     @param {GuildCreateManyArgs} args - Arguments to create many Guilds.
     *     @example
     *     // Create many Guilds
     *     const guild = await prisma.guild.createMany({
     *       data: {
     *         // ... provide data here
     *       }
     *     })
     *     
    **/
    createMany<T extends GuildCreateManyArgs>(
      args?: SelectSubset<T, GuildCreateManyArgs>
    ): Prisma.PrismaPromise<BatchPayload>

    /**
     * Delete a Guild.
     * @param {GuildDeleteArgs} args - Arguments to delete one Guild.
     * @example
     * // Delete one Guild
     * const Guild = await prisma.guild.delete({
     *   where: {
     *     // ... filter to delete one Guild
     *   }
     * })
     * 
    **/
    delete<T extends GuildDeleteArgs>(
      args: SelectSubset<T, GuildDeleteArgs>
    ): Prisma__GuildClient<GuildGetPayload<T>>

    /**
     * Update one Guild.
     * @param {GuildUpdateArgs} args - Arguments to update one Guild.
     * @example
     * // Update one Guild
     * const guild = await prisma.guild.update({
     *   where: {
     *     // ... provide filter here
     *   },
     *   data: {
     *     // ... provide data here
     *   }
     * })
     * 
    **/
    update<T extends GuildUpdateArgs>(
      args: SelectSubset<T, GuildUpdateArgs>
    ): Prisma__GuildClient<GuildGetPayload<T>>

    /**
     * Delete zero or more Guilds.
     * @param {GuildDeleteManyArgs} args - Arguments to filter Guilds to delete.
     * @example
     * // Delete a few Guilds
     * const { count } = await prisma.guild.deleteMany({
     *   where: {
     *     // ... provide filter here
     *   }
     * })
     * 
    **/
    deleteMany<T extends GuildDeleteManyArgs>(
      args?: SelectSubset<T, GuildDeleteManyArgs>
    ): Prisma.PrismaPromise<BatchPayload>

    /**
     * Update zero or more Guilds.
     * Note, that providing `undefined` is treated as the value not being there.
     * Read more here: https://pris.ly/d/null-undefined
     * @param {GuildUpdateManyArgs} args - Arguments to update one or more rows.
     * @example
     * // Update many Guilds
     * const guild = await prisma.guild.updateMany({
     *   where: {
     *     // ... provide filter here
     *   },
     *   data: {
     *     // ... provide data here
     *   }
     * })
     * 
    **/
    updateMany<T extends GuildUpdateManyArgs>(
      args: SelectSubset<T, GuildUpdateManyArgs>
    ): Prisma.PrismaPromise<BatchPayload>

    /**
     * Create or update one Guild.
     * @param {GuildUpsertArgs} args - Arguments to update or create a Guild.
     * @example
     * // Update or create a Guild
     * const guild = await prisma.guild.upsert({
     *   create: {
     *     // ... data to create a Guild
     *   },
     *   update: {
     *     // ... in case it already exists, update
     *   },
     *   where: {
     *     // ... the filter for the Guild we want to update
     *   }
     * })
    **/
    upsert<T extends GuildUpsertArgs>(
      args: SelectSubset<T, GuildUpsertArgs>
    ): Prisma__GuildClient<GuildGetPayload<T>>

    /**
     * Count the number of Guilds.
     * Note, that providing `undefined` is treated as the value not being there.
     * Read more here: https://pris.ly/d/null-undefined
     * @param {GuildCountArgs} args - Arguments to filter Guilds to count.
     * @example
     * // Count the number of Guilds
     * const count = await prisma.guild.count({
     *   where: {
     *     // ... the filter for the Guilds we want to count
     *   }
     * })
    **/
    count<T extends GuildCountArgs>(
      args?: Subset<T, GuildCountArgs>,
    ): Prisma.PrismaPromise<
      T extends _Record<'select', any>
        ? T['select'] extends true
          ? number
          : GetScalarType<T['select'], GuildCountAggregateOutputType>
        : number
    >

    /**
     * Allows you to perform aggregations operations on a Guild.
     * Note, that providing `undefined` is treated as the value not being there.
     * Read more here: https://pris.ly/d/null-undefined
     * @param {GuildAggregateArgs} args - Select which aggregations you would like to apply and on what fields.
     * @example
     * // Ordered by age ascending
     * // Where email contains prisma.io
     * // Limited to the 10 users
     * const aggregations = await prisma.user.aggregate({
     *   _avg: {
     *     age: true,
     *   },
     *   where: {
     *     email: {
     *       contains: "prisma.io",
     *     },
     *   },
     *   orderBy: {
     *     age: "asc",
     *   },
     *   take: 10,
     * })
    **/
    aggregate<T extends GuildAggregateArgs>(args: Subset<T, GuildAggregateArgs>): Prisma.PrismaPromise<GetGuildAggregateType<T>>

    /**
     * Group by Guild.
     * Note, that providing `undefined` is treated as the value not being there.
     * Read more here: https://pris.ly/d/null-undefined
     * @param {GuildGroupByArgs} args - Group by arguments.
     * @example
     * // Group by city, order by createdAt, get count
     * const result = await prisma.user.groupBy({
     *   by: ['city', 'createdAt'],
     *   orderBy: {
     *     createdAt: true
     *   },
     *   _count: {
     *     _all: true
     *   },
     * })
     * 
    **/
    groupBy<
      T extends GuildGroupByArgs,
      HasSelectOrTake extends Or<
        Extends<'skip', Keys<T>>,
        Extends<'take', Keys<T>>
      >,
      OrderByArg extends True extends HasSelectOrTake
        ? { orderBy: GuildGroupByArgs['orderBy'] }
        : { orderBy?: GuildGroupByArgs['orderBy'] },
      OrderFields extends ExcludeUnderscoreKeys<Keys<MaybeTupleToUnion<T['orderBy']>>>,
      ByFields extends TupleToUnion<T['by']>,
      ByValid extends Has<ByFields, OrderFields>,
      HavingFields extends GetHavingFields<T['having']>,
      HavingValid extends Has<ByFields, HavingFields>,
      ByEmpty extends T['by'] extends never[] ? True : False,
      InputErrors extends ByEmpty extends True
      ? `Error: "by" must not be empty.`
      : HavingValid extends False
      ? {
          [P in HavingFields]: P extends ByFields
            ? never
            : P extends string
            ? `Error: Field "${P}" used in "having" needs to be provided in "by".`
            : [
                Error,
                'Field ',
                P,
                ` in "having" needs to be provided in "by"`,
              ]
        }[HavingFields]
      : 'take' extends Keys<T>
      ? 'orderBy' extends Keys<T>
        ? ByValid extends True
          ? {}
          : {
              [P in OrderFields]: P extends ByFields
                ? never
                : `Error: Field "${P}" in "orderBy" needs to be provided in "by"`
            }[OrderFields]
        : 'Error: If you provide "take", you also need to provide "orderBy"'
      : 'skip' extends Keys<T>
      ? 'orderBy' extends Keys<T>
        ? ByValid extends True
          ? {}
          : {
              [P in OrderFields]: P extends ByFields
                ? never
                : `Error: Field "${P}" in "orderBy" needs to be provided in "by"`
            }[OrderFields]
        : 'Error: If you provide "skip", you also need to provide "orderBy"'
      : ByValid extends True
      ? {}
      : {
          [P in OrderFields]: P extends ByFields
            ? never
            : `Error: Field "${P}" in "orderBy" needs to be provided in "by"`
        }[OrderFields]
    >(args: SubsetIntersection<T, GuildGroupByArgs, OrderByArg> & InputErrors): {} extends InputErrors ? GetGuildGroupByPayload<T> : Prisma.PrismaPromise<InputErrors>

  }

  /**
   * The delegate class that acts as a "Promise-like" for Guild.
   * Why is this prefixed with `Prisma__`?
   * Because we want to prevent naming conflicts as mentioned in
   * https://github.com/prisma/prisma-client-js/issues/707
   */
  export class Prisma__GuildClient<T, Null = never> implements Prisma.PrismaPromise<T> {
    private readonly _dmmf;
    private readonly _queryType;
    private readonly _rootField;
    private readonly _clientMethod;
    private readonly _args;
    private readonly _dataPath;
    private readonly _errorFormat;
    private readonly _measurePerformance?;
    private _isList;
    private _callsite;
    private _requestPromise?;
    readonly [Symbol.toStringTag]: 'PrismaPromise';
    constructor(_dmmf: runtime.DMMFClass, _queryType: 'query' | 'mutation', _rootField: string, _clientMethod: string, _args: any, _dataPath: string[], _errorFormat: ErrorFormat, _measurePerformance?: boolean | undefined, _isList?: boolean);

    arts<T extends Guild$artsArgs= {}>(args?: Subset<T, Guild$artsArgs>): Prisma.PrismaPromise<Array<ArtGetPayload<T>>| Null>;

    vars<T extends Guild$varsArgs= {}>(args?: Subset<T, Guild$varsArgs>): Prisma.PrismaPromise<Array<VarialbleGetPayload<T>>| Null>;

    private get _document();
    /**
     * Attaches callbacks for the resolution and/or rejection of the Promise.
     * @param onfulfilled The callback to execute when the Promise is resolved.
     * @param onrejected The callback to execute when the Promise is rejected.
     * @returns A Promise for the completion of which ever callback is executed.
     */
    then<TResult1 = T, TResult2 = never>(onfulfilled?: ((value: T) => TResult1 | PromiseLike<TResult1>) | undefined | null, onrejected?: ((reason: any) => TResult2 | PromiseLike<TResult2>) | undefined | null): Promise<TResult1 | TResult2>;
    /**
     * Attaches a callback for only the rejection of the Promise.
     * @param onrejected The callback to execute when the Promise is rejected.
     * @returns A Promise for the completion of the callback.
     */
    catch<TResult = never>(onrejected?: ((reason: any) => TResult | PromiseLike<TResult>) | undefined | null): Promise<T | TResult>;
    /**
     * Attaches a callback that is invoked when the Promise is settled (fulfilled or rejected). The
     * resolved value cannot be modified from the callback.
     * @param onfinally The callback to execute when the Promise is settled (fulfilled or rejected).
     * @returns A Promise for the completion of the callback.
     */
    finally(onfinally?: (() => void) | undefined | null): Promise<T>;
  }



  // Custom InputTypes

  /**
   * Guild base type for findUnique actions
   */
  export type GuildFindUniqueArgsBase = {
    /**
     * Select specific fields to fetch from the Guild
     */
    select?: GuildSelect | null
    /**
     * Choose, which related nodes to fetch as well.
     */
    include?: GuildInclude | null
    /**
     * Filter, which Guild to fetch.
     */
    where: GuildWhereUniqueInput
  }

  /**
   * Guild findUnique
   */
  export interface GuildFindUniqueArgs extends GuildFindUniqueArgsBase {
   /**
    * Throw an Error if query returns no results
    * @deprecated since 4.0.0: use `findUniqueOrThrow` method instead
    */
    rejectOnNotFound?: RejectOnNotFound
  }
      

  /**
   * Guild findUniqueOrThrow
   */
  export type GuildFindUniqueOrThrowArgs = {
    /**
     * Select specific fields to fetch from the Guild
     */
    select?: GuildSelect | null
    /**
     * Choose, which related nodes to fetch as well.
     */
    include?: GuildInclude | null
    /**
     * Filter, which Guild to fetch.
     */
    where: GuildWhereUniqueInput
  }


  /**
   * Guild base type for findFirst actions
   */
  export type GuildFindFirstArgsBase = {
    /**
     * Select specific fields to fetch from the Guild
     */
    select?: GuildSelect | null
    /**
     * Choose, which related nodes to fetch as well.
     */
    include?: GuildInclude | null
    /**
     * Filter, which Guild to fetch.
     */
    where?: GuildWhereInput
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/sorting Sorting Docs}
     * 
     * Determine the order of Guilds to fetch.
     */
    orderBy?: Enumerable<GuildOrderByWithRelationInput>
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/pagination#cursor-based-pagination Cursor Docs}
     * 
     * Sets the position for searching for Guilds.
     */
    cursor?: GuildWhereUniqueInput
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/pagination Pagination Docs}
     * 
     * Take `±n` Guilds from the position of the cursor.
     */
    take?: number
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/pagination Pagination Docs}
     * 
     * Skip the first `n` Guilds.
     */
    skip?: number
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/distinct Distinct Docs}
     * 
     * Filter by unique combinations of Guilds.
     */
    distinct?: Enumerable<GuildScalarFieldEnum>
  }

  /**
   * Guild findFirst
   */
  export interface GuildFindFirstArgs extends GuildFindFirstArgsBase {
   /**
    * Throw an Error if query returns no results
    * @deprecated since 4.0.0: use `findFirstOrThrow` method instead
    */
    rejectOnNotFound?: RejectOnNotFound
  }
      

  /**
   * Guild findFirstOrThrow
   */
  export type GuildFindFirstOrThrowArgs = {
    /**
     * Select specific fields to fetch from the Guild
     */
    select?: GuildSelect | null
    /**
     * Choose, which related nodes to fetch as well.
     */
    include?: GuildInclude | null
    /**
     * Filter, which Guild to fetch.
     */
    where?: GuildWhereInput
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/sorting Sorting Docs}
     * 
     * Determine the order of Guilds to fetch.
     */
    orderBy?: Enumerable<GuildOrderByWithRelationInput>
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/pagination#cursor-based-pagination Cursor Docs}
     * 
     * Sets the position for searching for Guilds.
     */
    cursor?: GuildWhereUniqueInput
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/pagination Pagination Docs}
     * 
     * Take `±n` Guilds from the position of the cursor.
     */
    take?: number
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/pagination Pagination Docs}
     * 
     * Skip the first `n` Guilds.
     */
    skip?: number
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/distinct Distinct Docs}
     * 
     * Filter by unique combinations of Guilds.
     */
    distinct?: Enumerable<GuildScalarFieldEnum>
  }


  /**
   * Guild findMany
   */
  export type GuildFindManyArgs = {
    /**
     * Select specific fields to fetch from the Guild
     */
    select?: GuildSelect | null
    /**
     * Choose, which related nodes to fetch as well.
     */
    include?: GuildInclude | null
    /**
     * Filter, which Guilds to fetch.
     */
    where?: GuildWhereInput
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/sorting Sorting Docs}
     * 
     * Determine the order of Guilds to fetch.
     */
    orderBy?: Enumerable<GuildOrderByWithRelationInput>
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/pagination#cursor-based-pagination Cursor Docs}
     * 
     * Sets the position for listing Guilds.
     */
    cursor?: GuildWhereUniqueInput
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/pagination Pagination Docs}
     * 
     * Take `±n` Guilds from the position of the cursor.
     */
    take?: number
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/pagination Pagination Docs}
     * 
     * Skip the first `n` Guilds.
     */
    skip?: number
    distinct?: Enumerable<GuildScalarFieldEnum>
  }


  /**
   * Guild create
   */
  export type GuildCreateArgs = {
    /**
     * Select specific fields to fetch from the Guild
     */
    select?: GuildSelect | null
    /**
     * Choose, which related nodes to fetch as well.
     */
    include?: GuildInclude | null
    /**
     * The data needed to create a Guild.
     */
    data: XOR<GuildCreateInput, GuildUncheckedCreateInput>
  }


  /**
   * Guild createMany
   */
  export type GuildCreateManyArgs = {
    /**
     * The data used to create many Guilds.
     */
    data: Enumerable<GuildCreateManyInput>
    skipDuplicates?: boolean
  }


  /**
   * Guild update
   */
  export type GuildUpdateArgs = {
    /**
     * Select specific fields to fetch from the Guild
     */
    select?: GuildSelect | null
    /**
     * Choose, which related nodes to fetch as well.
     */
    include?: GuildInclude | null
    /**
     * The data needed to update a Guild.
     */
    data: XOR<GuildUpdateInput, GuildUncheckedUpdateInput>
    /**
     * Choose, which Guild to update.
     */
    where: GuildWhereUniqueInput
  }


  /**
   * Guild updateMany
   */
  export type GuildUpdateManyArgs = {
    /**
     * The data used to update Guilds.
     */
    data: XOR<GuildUpdateManyMutationInput, GuildUncheckedUpdateManyInput>
    /**
     * Filter which Guilds to update
     */
    where?: GuildWhereInput
  }


  /**
   * Guild upsert
   */
  export type GuildUpsertArgs = {
    /**
     * Select specific fields to fetch from the Guild
     */
    select?: GuildSelect | null
    /**
     * Choose, which related nodes to fetch as well.
     */
    include?: GuildInclude | null
    /**
     * The filter to search for the Guild to update in case it exists.
     */
    where: GuildWhereUniqueInput
    /**
     * In case the Guild found by the `where` argument doesn't exist, create a new Guild with this data.
     */
    create: XOR<GuildCreateInput, GuildUncheckedCreateInput>
    /**
     * In case the Guild was found with the provided `where` argument, update it with this data.
     */
    update: XOR<GuildUpdateInput, GuildUncheckedUpdateInput>
  }


  /**
   * Guild delete
   */
  export type GuildDeleteArgs = {
    /**
     * Select specific fields to fetch from the Guild
     */
    select?: GuildSelect | null
    /**
     * Choose, which related nodes to fetch as well.
     */
    include?: GuildInclude | null
    /**
     * Filter which Guild to delete.
     */
    where: GuildWhereUniqueInput
  }


  /**
   * Guild deleteMany
   */
  export type GuildDeleteManyArgs = {
    /**
     * Filter which Guilds to delete
     */
    where?: GuildWhereInput
  }


  /**
   * Guild.arts
   */
  export type Guild$artsArgs = {
    /**
     * Select specific fields to fetch from the Art
     */
    select?: ArtSelect | null
    /**
     * Choose, which related nodes to fetch as well.
     */
    include?: ArtInclude | null
    where?: ArtWhereInput
    orderBy?: Enumerable<ArtOrderByWithRelationInput>
    cursor?: ArtWhereUniqueInput
    take?: number
    skip?: number
    distinct?: Enumerable<ArtScalarFieldEnum>
  }


  /**
   * Guild.vars
   */
  export type Guild$varsArgs = {
    /**
     * Select specific fields to fetch from the Varialble
     */
    select?: VarialbleSelect | null
    /**
     * Choose, which related nodes to fetch as well.
     */
    include?: VarialbleInclude | null
    where?: VarialbleWhereInput
    orderBy?: Enumerable<VarialbleOrderByWithRelationInput>
    cursor?: VarialbleWhereUniqueInput
    take?: number
    skip?: number
    distinct?: Enumerable<VarialbleScalarFieldEnum>
  }


  /**
   * Guild without action
   */
  export type GuildArgs = {
    /**
     * Select specific fields to fetch from the Guild
     */
    select?: GuildSelect | null
    /**
     * Choose, which related nodes to fetch as well.
     */
    include?: GuildInclude | null
  }



  /**
   * Model Art
   */


  export type AggregateArt = {
    _count: ArtCountAggregateOutputType | null
    _min: ArtMinAggregateOutputType | null
    _max: ArtMaxAggregateOutputType | null
  }

  export type ArtMinAggregateOutputType = {
    name: string | null
    key: string | null
    type: ArtType | null
    role: string | null
    guild_id: string | null
    embed_title: string | null
    embed_description: string | null
    embed_url: string | null
    created_at: Date | null
    updated_at: Date | null
  }

  export type ArtMaxAggregateOutputType = {
    name: string | null
    key: string | null
    type: ArtType | null
    role: string | null
    guild_id: string | null
    embed_title: string | null
    embed_description: string | null
    embed_url: string | null
    created_at: Date | null
    updated_at: Date | null
  }

  export type ArtCountAggregateOutputType = {
    name: number
    key: number
    type: number
    role: number
    guild_id: number
    embed_title: number
    embed_description: number
    embed_url: number
    created_at: number
    updated_at: number
    _all: number
  }


  export type ArtMinAggregateInputType = {
    name?: true
    key?: true
    type?: true
    role?: true
    guild_id?: true
    embed_title?: true
    embed_description?: true
    embed_url?: true
    created_at?: true
    updated_at?: true
  }

  export type ArtMaxAggregateInputType = {
    name?: true
    key?: true
    type?: true
    role?: true
    guild_id?: true
    embed_title?: true
    embed_description?: true
    embed_url?: true
    created_at?: true
    updated_at?: true
  }

  export type ArtCountAggregateInputType = {
    name?: true
    key?: true
    type?: true
    role?: true
    guild_id?: true
    embed_title?: true
    embed_description?: true
    embed_url?: true
    created_at?: true
    updated_at?: true
    _all?: true
  }

  export type ArtAggregateArgs = {
    /**
     * Filter which Art to aggregate.
     */
    where?: ArtWhereInput
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/sorting Sorting Docs}
     * 
     * Determine the order of Arts to fetch.
     */
    orderBy?: Enumerable<ArtOrderByWithRelationInput>
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/pagination#cursor-based-pagination Cursor Docs}
     * 
     * Sets the start position
     */
    cursor?: ArtWhereUniqueInput
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/pagination Pagination Docs}
     * 
     * Take `±n` Arts from the position of the cursor.
     */
    take?: number
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/pagination Pagination Docs}
     * 
     * Skip the first `n` Arts.
     */
    skip?: number
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/aggregations Aggregation Docs}
     * 
     * Count returned Arts
    **/
    _count?: true | ArtCountAggregateInputType
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/aggregations Aggregation Docs}
     * 
     * Select which fields to find the minimum value
    **/
    _min?: ArtMinAggregateInputType
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/aggregations Aggregation Docs}
     * 
     * Select which fields to find the maximum value
    **/
    _max?: ArtMaxAggregateInputType
  }

  export type GetArtAggregateType<T extends ArtAggregateArgs> = {
        [P in keyof T & keyof AggregateArt]: P extends '_count' | 'count'
      ? T[P] extends true
        ? number
        : GetScalarType<T[P], AggregateArt[P]>
      : GetScalarType<T[P], AggregateArt[P]>
  }




  export type ArtGroupByArgs = {
    where?: ArtWhereInput
    orderBy?: Enumerable<ArtOrderByWithAggregationInput>
    by: ArtScalarFieldEnum[]
    having?: ArtScalarWhereWithAggregatesInput
    take?: number
    skip?: number
    _count?: ArtCountAggregateInputType | true
    _min?: ArtMinAggregateInputType
    _max?: ArtMaxAggregateInputType
  }


  export type ArtGroupByOutputType = {
    name: string
    key: string
    type: ArtType
    role: string | null
    guild_id: string
    embed_title: string | null
    embed_description: string | null
    embed_url: string | null
    created_at: Date
    updated_at: Date
    _count: ArtCountAggregateOutputType | null
    _min: ArtMinAggregateOutputType | null
    _max: ArtMaxAggregateOutputType | null
  }

  type GetArtGroupByPayload<T extends ArtGroupByArgs> = Prisma.PrismaPromise<
    Array<
      PickArray<ArtGroupByOutputType, T['by']> &
        {
          [P in ((keyof T) & (keyof ArtGroupByOutputType))]: P extends '_count'
            ? T[P] extends boolean
              ? number
              : GetScalarType<T[P], ArtGroupByOutputType[P]>
            : GetScalarType<T[P], ArtGroupByOutputType[P]>
        }
      >
    >


  export type ArtSelect = {
    name?: boolean
    key?: boolean
    type?: boolean
    role?: boolean
    guild_id?: boolean
    embed_title?: boolean
    embed_description?: boolean
    embed_url?: boolean
    created_at?: boolean
    updated_at?: boolean
    guild?: boolean | GuildArgs
    attacks?: boolean | Art$attacksArgs
    _count?: boolean | ArtCountOutputTypeArgs
  }


  export type ArtInclude = {
    guild?: boolean | GuildArgs
    attacks?: boolean | Art$attacksArgs
    _count?: boolean | ArtCountOutputTypeArgs
  }

  export type ArtGetPayload<S extends boolean | null | undefined | ArtArgs> =
    S extends { select: any, include: any } ? 'Please either choose `select` or `include`' :
    S extends true ? Art :
    S extends undefined ? never :
    S extends { include: any } & (ArtArgs | ArtFindManyArgs)
    ? Art  & {
    [P in TruthyKeys<S['include']>]:
        P extends 'guild' ? GuildGetPayload<S['include'][P]> :
        P extends 'attacks' ? Array < AttackGetPayload<S['include'][P]>>  :
        P extends '_count' ? ArtCountOutputTypeGetPayload<S['include'][P]> :  never
  } 
    : S extends { select: any } & (ArtArgs | ArtFindManyArgs)
      ? {
    [P in TruthyKeys<S['select']>]:
        P extends 'guild' ? GuildGetPayload<S['select'][P]> :
        P extends 'attacks' ? Array < AttackGetPayload<S['select'][P]>>  :
        P extends '_count' ? ArtCountOutputTypeGetPayload<S['select'][P]> :  P extends keyof Art ? Art[P] : never
  } 
      : Art


  type ArtCountArgs = 
    Omit<ArtFindManyArgs, 'select' | 'include'> & {
      select?: ArtCountAggregateInputType | true
    }

  export interface ArtDelegate<GlobalRejectSettings extends Prisma.RejectOnNotFound | Prisma.RejectPerOperation | false | undefined> {

    /**
     * Find zero or one Art that matches the filter.
     * @param {ArtFindUniqueArgs} args - Arguments to find a Art
     * @example
     * // Get one Art
     * const art = await prisma.art.findUnique({
     *   where: {
     *     // ... provide filter here
     *   }
     * })
    **/
    findUnique<T extends ArtFindUniqueArgs,  LocalRejectSettings = T["rejectOnNotFound"] extends RejectOnNotFound ? T['rejectOnNotFound'] : undefined>(
      args: SelectSubset<T, ArtFindUniqueArgs>
    ): HasReject<GlobalRejectSettings, LocalRejectSettings, 'findUnique', 'Art'> extends True ? Prisma__ArtClient<ArtGetPayload<T>> : Prisma__ArtClient<ArtGetPayload<T> | null, null>

    /**
     * Find one Art that matches the filter or throw an error  with `error.code='P2025'` 
     *     if no matches were found.
     * @param {ArtFindUniqueOrThrowArgs} args - Arguments to find a Art
     * @example
     * // Get one Art
     * const art = await prisma.art.findUniqueOrThrow({
     *   where: {
     *     // ... provide filter here
     *   }
     * })
    **/
    findUniqueOrThrow<T extends ArtFindUniqueOrThrowArgs>(
      args?: SelectSubset<T, ArtFindUniqueOrThrowArgs>
    ): Prisma__ArtClient<ArtGetPayload<T>>

    /**
     * Find the first Art that matches the filter.
     * Note, that providing `undefined` is treated as the value not being there.
     * Read more here: https://pris.ly/d/null-undefined
     * @param {ArtFindFirstArgs} args - Arguments to find a Art
     * @example
     * // Get one Art
     * const art = await prisma.art.findFirst({
     *   where: {
     *     // ... provide filter here
     *   }
     * })
    **/
    findFirst<T extends ArtFindFirstArgs,  LocalRejectSettings = T["rejectOnNotFound"] extends RejectOnNotFound ? T['rejectOnNotFound'] : undefined>(
      args?: SelectSubset<T, ArtFindFirstArgs>
    ): HasReject<GlobalRejectSettings, LocalRejectSettings, 'findFirst', 'Art'> extends True ? Prisma__ArtClient<ArtGetPayload<T>> : Prisma__ArtClient<ArtGetPayload<T> | null, null>

    /**
     * Find the first Art that matches the filter or
     * throw `NotFoundError` if no matches were found.
     * Note, that providing `undefined` is treated as the value not being there.
     * Read more here: https://pris.ly/d/null-undefined
     * @param {ArtFindFirstOrThrowArgs} args - Arguments to find a Art
     * @example
     * // Get one Art
     * const art = await prisma.art.findFirstOrThrow({
     *   where: {
     *     // ... provide filter here
     *   }
     * })
    **/
    findFirstOrThrow<T extends ArtFindFirstOrThrowArgs>(
      args?: SelectSubset<T, ArtFindFirstOrThrowArgs>
    ): Prisma__ArtClient<ArtGetPayload<T>>

    /**
     * Find zero or more Arts that matches the filter.
     * Note, that providing `undefined` is treated as the value not being there.
     * Read more here: https://pris.ly/d/null-undefined
     * @param {ArtFindManyArgs=} args - Arguments to filter and select certain fields only.
     * @example
     * // Get all Arts
     * const arts = await prisma.art.findMany()
     * 
     * // Get first 10 Arts
     * const arts = await prisma.art.findMany({ take: 10 })
     * 
     * // Only select the `name`
     * const artWithNameOnly = await prisma.art.findMany({ select: { name: true } })
     * 
    **/
    findMany<T extends ArtFindManyArgs>(
      args?: SelectSubset<T, ArtFindManyArgs>
    ): Prisma.PrismaPromise<Array<ArtGetPayload<T>>>

    /**
     * Create a Art.
     * @param {ArtCreateArgs} args - Arguments to create a Art.
     * @example
     * // Create one Art
     * const Art = await prisma.art.create({
     *   data: {
     *     // ... data to create a Art
     *   }
     * })
     * 
    **/
    create<T extends ArtCreateArgs>(
      args: SelectSubset<T, ArtCreateArgs>
    ): Prisma__ArtClient<ArtGetPayload<T>>

    /**
     * Create many Arts.
     *     @param {ArtCreateManyArgs} args - Arguments to create many Arts.
     *     @example
     *     // Create many Arts
     *     const art = await prisma.art.createMany({
     *       data: {
     *         // ... provide data here
     *       }
     *     })
     *     
    **/
    createMany<T extends ArtCreateManyArgs>(
      args?: SelectSubset<T, ArtCreateManyArgs>
    ): Prisma.PrismaPromise<BatchPayload>

    /**
     * Delete a Art.
     * @param {ArtDeleteArgs} args - Arguments to delete one Art.
     * @example
     * // Delete one Art
     * const Art = await prisma.art.delete({
     *   where: {
     *     // ... filter to delete one Art
     *   }
     * })
     * 
    **/
    delete<T extends ArtDeleteArgs>(
      args: SelectSubset<T, ArtDeleteArgs>
    ): Prisma__ArtClient<ArtGetPayload<T>>

    /**
     * Update one Art.
     * @param {ArtUpdateArgs} args - Arguments to update one Art.
     * @example
     * // Update one Art
     * const art = await prisma.art.update({
     *   where: {
     *     // ... provide filter here
     *   },
     *   data: {
     *     // ... provide data here
     *   }
     * })
     * 
    **/
    update<T extends ArtUpdateArgs>(
      args: SelectSubset<T, ArtUpdateArgs>
    ): Prisma__ArtClient<ArtGetPayload<T>>

    /**
     * Delete zero or more Arts.
     * @param {ArtDeleteManyArgs} args - Arguments to filter Arts to delete.
     * @example
     * // Delete a few Arts
     * const { count } = await prisma.art.deleteMany({
     *   where: {
     *     // ... provide filter here
     *   }
     * })
     * 
    **/
    deleteMany<T extends ArtDeleteManyArgs>(
      args?: SelectSubset<T, ArtDeleteManyArgs>
    ): Prisma.PrismaPromise<BatchPayload>

    /**
     * Update zero or more Arts.
     * Note, that providing `undefined` is treated as the value not being there.
     * Read more here: https://pris.ly/d/null-undefined
     * @param {ArtUpdateManyArgs} args - Arguments to update one or more rows.
     * @example
     * // Update many Arts
     * const art = await prisma.art.updateMany({
     *   where: {
     *     // ... provide filter here
     *   },
     *   data: {
     *     // ... provide data here
     *   }
     * })
     * 
    **/
    updateMany<T extends ArtUpdateManyArgs>(
      args: SelectSubset<T, ArtUpdateManyArgs>
    ): Prisma.PrismaPromise<BatchPayload>

    /**
     * Create or update one Art.
     * @param {ArtUpsertArgs} args - Arguments to update or create a Art.
     * @example
     * // Update or create a Art
     * const art = await prisma.art.upsert({
     *   create: {
     *     // ... data to create a Art
     *   },
     *   update: {
     *     // ... in case it already exists, update
     *   },
     *   where: {
     *     // ... the filter for the Art we want to update
     *   }
     * })
    **/
    upsert<T extends ArtUpsertArgs>(
      args: SelectSubset<T, ArtUpsertArgs>
    ): Prisma__ArtClient<ArtGetPayload<T>>

    /**
     * Count the number of Arts.
     * Note, that providing `undefined` is treated as the value not being there.
     * Read more here: https://pris.ly/d/null-undefined
     * @param {ArtCountArgs} args - Arguments to filter Arts to count.
     * @example
     * // Count the number of Arts
     * const count = await prisma.art.count({
     *   where: {
     *     // ... the filter for the Arts we want to count
     *   }
     * })
    **/
    count<T extends ArtCountArgs>(
      args?: Subset<T, ArtCountArgs>,
    ): Prisma.PrismaPromise<
      T extends _Record<'select', any>
        ? T['select'] extends true
          ? number
          : GetScalarType<T['select'], ArtCountAggregateOutputType>
        : number
    >

    /**
     * Allows you to perform aggregations operations on a Art.
     * Note, that providing `undefined` is treated as the value not being there.
     * Read more here: https://pris.ly/d/null-undefined
     * @param {ArtAggregateArgs} args - Select which aggregations you would like to apply and on what fields.
     * @example
     * // Ordered by age ascending
     * // Where email contains prisma.io
     * // Limited to the 10 users
     * const aggregations = await prisma.user.aggregate({
     *   _avg: {
     *     age: true,
     *   },
     *   where: {
     *     email: {
     *       contains: "prisma.io",
     *     },
     *   },
     *   orderBy: {
     *     age: "asc",
     *   },
     *   take: 10,
     * })
    **/
    aggregate<T extends ArtAggregateArgs>(args: Subset<T, ArtAggregateArgs>): Prisma.PrismaPromise<GetArtAggregateType<T>>

    /**
     * Group by Art.
     * Note, that providing `undefined` is treated as the value not being there.
     * Read more here: https://pris.ly/d/null-undefined
     * @param {ArtGroupByArgs} args - Group by arguments.
     * @example
     * // Group by city, order by createdAt, get count
     * const result = await prisma.user.groupBy({
     *   by: ['city', 'createdAt'],
     *   orderBy: {
     *     createdAt: true
     *   },
     *   _count: {
     *     _all: true
     *   },
     * })
     * 
    **/
    groupBy<
      T extends ArtGroupByArgs,
      HasSelectOrTake extends Or<
        Extends<'skip', Keys<T>>,
        Extends<'take', Keys<T>>
      >,
      OrderByArg extends True extends HasSelectOrTake
        ? { orderBy: ArtGroupByArgs['orderBy'] }
        : { orderBy?: ArtGroupByArgs['orderBy'] },
      OrderFields extends ExcludeUnderscoreKeys<Keys<MaybeTupleToUnion<T['orderBy']>>>,
      ByFields extends TupleToUnion<T['by']>,
      ByValid extends Has<ByFields, OrderFields>,
      HavingFields extends GetHavingFields<T['having']>,
      HavingValid extends Has<ByFields, HavingFields>,
      ByEmpty extends T['by'] extends never[] ? True : False,
      InputErrors extends ByEmpty extends True
      ? `Error: "by" must not be empty.`
      : HavingValid extends False
      ? {
          [P in HavingFields]: P extends ByFields
            ? never
            : P extends string
            ? `Error: Field "${P}" used in "having" needs to be provided in "by".`
            : [
                Error,
                'Field ',
                P,
                ` in "having" needs to be provided in "by"`,
              ]
        }[HavingFields]
      : 'take' extends Keys<T>
      ? 'orderBy' extends Keys<T>
        ? ByValid extends True
          ? {}
          : {
              [P in OrderFields]: P extends ByFields
                ? never
                : `Error: Field "${P}" in "orderBy" needs to be provided in "by"`
            }[OrderFields]
        : 'Error: If you provide "take", you also need to provide "orderBy"'
      : 'skip' extends Keys<T>
      ? 'orderBy' extends Keys<T>
        ? ByValid extends True
          ? {}
          : {
              [P in OrderFields]: P extends ByFields
                ? never
                : `Error: Field "${P}" in "orderBy" needs to be provided in "by"`
            }[OrderFields]
        : 'Error: If you provide "skip", you also need to provide "orderBy"'
      : ByValid extends True
      ? {}
      : {
          [P in OrderFields]: P extends ByFields
            ? never
            : `Error: Field "${P}" in "orderBy" needs to be provided in "by"`
        }[OrderFields]
    >(args: SubsetIntersection<T, ArtGroupByArgs, OrderByArg> & InputErrors): {} extends InputErrors ? GetArtGroupByPayload<T> : Prisma.PrismaPromise<InputErrors>

  }

  /**
   * The delegate class that acts as a "Promise-like" for Art.
   * Why is this prefixed with `Prisma__`?
   * Because we want to prevent naming conflicts as mentioned in
   * https://github.com/prisma/prisma-client-js/issues/707
   */
  export class Prisma__ArtClient<T, Null = never> implements Prisma.PrismaPromise<T> {
    private readonly _dmmf;
    private readonly _queryType;
    private readonly _rootField;
    private readonly _clientMethod;
    private readonly _args;
    private readonly _dataPath;
    private readonly _errorFormat;
    private readonly _measurePerformance?;
    private _isList;
    private _callsite;
    private _requestPromise?;
    readonly [Symbol.toStringTag]: 'PrismaPromise';
    constructor(_dmmf: runtime.DMMFClass, _queryType: 'query' | 'mutation', _rootField: string, _clientMethod: string, _args: any, _dataPath: string[], _errorFormat: ErrorFormat, _measurePerformance?: boolean | undefined, _isList?: boolean);

    guild<T extends GuildArgs= {}>(args?: Subset<T, GuildArgs>): Prisma__GuildClient<GuildGetPayload<T> | Null>;

    attacks<T extends Art$attacksArgs= {}>(args?: Subset<T, Art$attacksArgs>): Prisma.PrismaPromise<Array<AttackGetPayload<T>>| Null>;

    private get _document();
    /**
     * Attaches callbacks for the resolution and/or rejection of the Promise.
     * @param onfulfilled The callback to execute when the Promise is resolved.
     * @param onrejected The callback to execute when the Promise is rejected.
     * @returns A Promise for the completion of which ever callback is executed.
     */
    then<TResult1 = T, TResult2 = never>(onfulfilled?: ((value: T) => TResult1 | PromiseLike<TResult1>) | undefined | null, onrejected?: ((reason: any) => TResult2 | PromiseLike<TResult2>) | undefined | null): Promise<TResult1 | TResult2>;
    /**
     * Attaches a callback for only the rejection of the Promise.
     * @param onrejected The callback to execute when the Promise is rejected.
     * @returns A Promise for the completion of the callback.
     */
    catch<TResult = never>(onrejected?: ((reason: any) => TResult | PromiseLike<TResult>) | undefined | null): Promise<T | TResult>;
    /**
     * Attaches a callback that is invoked when the Promise is settled (fulfilled or rejected). The
     * resolved value cannot be modified from the callback.
     * @param onfinally The callback to execute when the Promise is settled (fulfilled or rejected).
     * @returns A Promise for the completion of the callback.
     */
    finally(onfinally?: (() => void) | undefined | null): Promise<T>;
  }



  // Custom InputTypes

  /**
   * Art base type for findUnique actions
   */
  export type ArtFindUniqueArgsBase = {
    /**
     * Select specific fields to fetch from the Art
     */
    select?: ArtSelect | null
    /**
     * Choose, which related nodes to fetch as well.
     */
    include?: ArtInclude | null
    /**
     * Filter, which Art to fetch.
     */
    where: ArtWhereUniqueInput
  }

  /**
   * Art findUnique
   */
  export interface ArtFindUniqueArgs extends ArtFindUniqueArgsBase {
   /**
    * Throw an Error if query returns no results
    * @deprecated since 4.0.0: use `findUniqueOrThrow` method instead
    */
    rejectOnNotFound?: RejectOnNotFound
  }
      

  /**
   * Art findUniqueOrThrow
   */
  export type ArtFindUniqueOrThrowArgs = {
    /**
     * Select specific fields to fetch from the Art
     */
    select?: ArtSelect | null
    /**
     * Choose, which related nodes to fetch as well.
     */
    include?: ArtInclude | null
    /**
     * Filter, which Art to fetch.
     */
    where: ArtWhereUniqueInput
  }


  /**
   * Art base type for findFirst actions
   */
  export type ArtFindFirstArgsBase = {
    /**
     * Select specific fields to fetch from the Art
     */
    select?: ArtSelect | null
    /**
     * Choose, which related nodes to fetch as well.
     */
    include?: ArtInclude | null
    /**
     * Filter, which Art to fetch.
     */
    where?: ArtWhereInput
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/sorting Sorting Docs}
     * 
     * Determine the order of Arts to fetch.
     */
    orderBy?: Enumerable<ArtOrderByWithRelationInput>
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/pagination#cursor-based-pagination Cursor Docs}
     * 
     * Sets the position for searching for Arts.
     */
    cursor?: ArtWhereUniqueInput
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/pagination Pagination Docs}
     * 
     * Take `±n` Arts from the position of the cursor.
     */
    take?: number
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/pagination Pagination Docs}
     * 
     * Skip the first `n` Arts.
     */
    skip?: number
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/distinct Distinct Docs}
     * 
     * Filter by unique combinations of Arts.
     */
    distinct?: Enumerable<ArtScalarFieldEnum>
  }

  /**
   * Art findFirst
   */
  export interface ArtFindFirstArgs extends ArtFindFirstArgsBase {
   /**
    * Throw an Error if query returns no results
    * @deprecated since 4.0.0: use `findFirstOrThrow` method instead
    */
    rejectOnNotFound?: RejectOnNotFound
  }
      

  /**
   * Art findFirstOrThrow
   */
  export type ArtFindFirstOrThrowArgs = {
    /**
     * Select specific fields to fetch from the Art
     */
    select?: ArtSelect | null
    /**
     * Choose, which related nodes to fetch as well.
     */
    include?: ArtInclude | null
    /**
     * Filter, which Art to fetch.
     */
    where?: ArtWhereInput
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/sorting Sorting Docs}
     * 
     * Determine the order of Arts to fetch.
     */
    orderBy?: Enumerable<ArtOrderByWithRelationInput>
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/pagination#cursor-based-pagination Cursor Docs}
     * 
     * Sets the position for searching for Arts.
     */
    cursor?: ArtWhereUniqueInput
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/pagination Pagination Docs}
     * 
     * Take `±n` Arts from the position of the cursor.
     */
    take?: number
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/pagination Pagination Docs}
     * 
     * Skip the first `n` Arts.
     */
    skip?: number
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/distinct Distinct Docs}
     * 
     * Filter by unique combinations of Arts.
     */
    distinct?: Enumerable<ArtScalarFieldEnum>
  }


  /**
   * Art findMany
   */
  export type ArtFindManyArgs = {
    /**
     * Select specific fields to fetch from the Art
     */
    select?: ArtSelect | null
    /**
     * Choose, which related nodes to fetch as well.
     */
    include?: ArtInclude | null
    /**
     * Filter, which Arts to fetch.
     */
    where?: ArtWhereInput
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/sorting Sorting Docs}
     * 
     * Determine the order of Arts to fetch.
     */
    orderBy?: Enumerable<ArtOrderByWithRelationInput>
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/pagination#cursor-based-pagination Cursor Docs}
     * 
     * Sets the position for listing Arts.
     */
    cursor?: ArtWhereUniqueInput
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/pagination Pagination Docs}
     * 
     * Take `±n` Arts from the position of the cursor.
     */
    take?: number
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/pagination Pagination Docs}
     * 
     * Skip the first `n` Arts.
     */
    skip?: number
    distinct?: Enumerable<ArtScalarFieldEnum>
  }


  /**
   * Art create
   */
  export type ArtCreateArgs = {
    /**
     * Select specific fields to fetch from the Art
     */
    select?: ArtSelect | null
    /**
     * Choose, which related nodes to fetch as well.
     */
    include?: ArtInclude | null
    /**
     * The data needed to create a Art.
     */
    data: XOR<ArtCreateInput, ArtUncheckedCreateInput>
  }


  /**
   * Art createMany
   */
  export type ArtCreateManyArgs = {
    /**
     * The data used to create many Arts.
     */
    data: Enumerable<ArtCreateManyInput>
    skipDuplicates?: boolean
  }


  /**
   * Art update
   */
  export type ArtUpdateArgs = {
    /**
     * Select specific fields to fetch from the Art
     */
    select?: ArtSelect | null
    /**
     * Choose, which related nodes to fetch as well.
     */
    include?: ArtInclude | null
    /**
     * The data needed to update a Art.
     */
    data: XOR<ArtUpdateInput, ArtUncheckedUpdateInput>
    /**
     * Choose, which Art to update.
     */
    where: ArtWhereUniqueInput
  }


  /**
   * Art updateMany
   */
  export type ArtUpdateManyArgs = {
    /**
     * The data used to update Arts.
     */
    data: XOR<ArtUpdateManyMutationInput, ArtUncheckedUpdateManyInput>
    /**
     * Filter which Arts to update
     */
    where?: ArtWhereInput
  }


  /**
   * Art upsert
   */
  export type ArtUpsertArgs = {
    /**
     * Select specific fields to fetch from the Art
     */
    select?: ArtSelect | null
    /**
     * Choose, which related nodes to fetch as well.
     */
    include?: ArtInclude | null
    /**
     * The filter to search for the Art to update in case it exists.
     */
    where: ArtWhereUniqueInput
    /**
     * In case the Art found by the `where` argument doesn't exist, create a new Art with this data.
     */
    create: XOR<ArtCreateInput, ArtUncheckedCreateInput>
    /**
     * In case the Art was found with the provided `where` argument, update it with this data.
     */
    update: XOR<ArtUpdateInput, ArtUncheckedUpdateInput>
  }


  /**
   * Art delete
   */
  export type ArtDeleteArgs = {
    /**
     * Select specific fields to fetch from the Art
     */
    select?: ArtSelect | null
    /**
     * Choose, which related nodes to fetch as well.
     */
    include?: ArtInclude | null
    /**
     * Filter which Art to delete.
     */
    where: ArtWhereUniqueInput
  }


  /**
   * Art deleteMany
   */
  export type ArtDeleteManyArgs = {
    /**
     * Filter which Arts to delete
     */
    where?: ArtWhereInput
  }


  /**
   * Art.attacks
   */
  export type Art$attacksArgs = {
    /**
     * Select specific fields to fetch from the Attack
     */
    select?: AttackSelect | null
    /**
     * Choose, which related nodes to fetch as well.
     */
    include?: AttackInclude | null
    where?: AttackWhereInput
    orderBy?: Enumerable<AttackOrderByWithRelationInput>
    cursor?: AttackWhereUniqueInput
    take?: number
    skip?: number
    distinct?: Enumerable<AttackScalarFieldEnum>
  }


  /**
   * Art without action
   */
  export type ArtArgs = {
    /**
     * Select specific fields to fetch from the Art
     */
    select?: ArtSelect | null
    /**
     * Choose, which related nodes to fetch as well.
     */
    include?: ArtInclude | null
  }



  /**
   * Model Attack
   */


  export type AggregateAttack = {
    _count: AttackCountAggregateOutputType | null
    _avg: AttackAvgAggregateOutputType | null
    _sum: AttackSumAggregateOutputType | null
    _min: AttackMinAggregateOutputType | null
    _max: AttackMaxAggregateOutputType | null
  }

  export type AttackAvgAggregateOutputType = {
    required_roles: number | null
    required_exp: number | null
    damage: number | null
    stamina: number | null
  }

  export type AttackSumAggregateOutputType = {
    required_roles: number | null
    required_exp: number | null
    damage: number | null
    stamina: number | null
  }

  export type AttackMinAggregateOutputType = {
    name: string | null
    key: string | null
    art_key: string | null
    guild_id: string | null
    required_roles: number | null
    required_exp: number | null
    damage: number | null
    stamina: number | null
    embed_title: string | null
    embed_description: string | null
    embed_url: string | null
    fields_key: string | null
    created_at: Date | null
    updated_at: Date | null
  }

  export type AttackMaxAggregateOutputType = {
    name: string | null
    key: string | null
    art_key: string | null
    guild_id: string | null
    required_roles: number | null
    required_exp: number | null
    damage: number | null
    stamina: number | null
    embed_title: string | null
    embed_description: string | null
    embed_url: string | null
    fields_key: string | null
    created_at: Date | null
    updated_at: Date | null
  }

  export type AttackCountAggregateOutputType = {
    name: number
    key: number
    art_key: number
    guild_id: number
    roles: number
    required_roles: number
    required_exp: number
    damage: number
    stamina: number
    embed_title: number
    embed_description: number
    embed_url: number
    fields_key: number
    created_at: number
    updated_at: number
    _all: number
  }


  export type AttackAvgAggregateInputType = {
    required_roles?: true
    required_exp?: true
    damage?: true
    stamina?: true
  }

  export type AttackSumAggregateInputType = {
    required_roles?: true
    required_exp?: true
    damage?: true
    stamina?: true
  }

  export type AttackMinAggregateInputType = {
    name?: true
    key?: true
    art_key?: true
    guild_id?: true
    required_roles?: true
    required_exp?: true
    damage?: true
    stamina?: true
    embed_title?: true
    embed_description?: true
    embed_url?: true
    fields_key?: true
    created_at?: true
    updated_at?: true
  }

  export type AttackMaxAggregateInputType = {
    name?: true
    key?: true
    art_key?: true
    guild_id?: true
    required_roles?: true
    required_exp?: true
    damage?: true
    stamina?: true
    embed_title?: true
    embed_description?: true
    embed_url?: true
    fields_key?: true
    created_at?: true
    updated_at?: true
  }

  export type AttackCountAggregateInputType = {
    name?: true
    key?: true
    art_key?: true
    guild_id?: true
    roles?: true
    required_roles?: true
    required_exp?: true
    damage?: true
    stamina?: true
    embed_title?: true
    embed_description?: true
    embed_url?: true
    fields_key?: true
    created_at?: true
    updated_at?: true
    _all?: true
  }

  export type AttackAggregateArgs = {
    /**
     * Filter which Attack to aggregate.
     */
    where?: AttackWhereInput
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/sorting Sorting Docs}
     * 
     * Determine the order of Attacks to fetch.
     */
    orderBy?: Enumerable<AttackOrderByWithRelationInput>
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/pagination#cursor-based-pagination Cursor Docs}
     * 
     * Sets the start position
     */
    cursor?: AttackWhereUniqueInput
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/pagination Pagination Docs}
     * 
     * Take `±n` Attacks from the position of the cursor.
     */
    take?: number
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/pagination Pagination Docs}
     * 
     * Skip the first `n` Attacks.
     */
    skip?: number
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/aggregations Aggregation Docs}
     * 
     * Count returned Attacks
    **/
    _count?: true | AttackCountAggregateInputType
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/aggregations Aggregation Docs}
     * 
     * Select which fields to average
    **/
    _avg?: AttackAvgAggregateInputType
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/aggregations Aggregation Docs}
     * 
     * Select which fields to sum
    **/
    _sum?: AttackSumAggregateInputType
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/aggregations Aggregation Docs}
     * 
     * Select which fields to find the minimum value
    **/
    _min?: AttackMinAggregateInputType
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/aggregations Aggregation Docs}
     * 
     * Select which fields to find the maximum value
    **/
    _max?: AttackMaxAggregateInputType
  }

  export type GetAttackAggregateType<T extends AttackAggregateArgs> = {
        [P in keyof T & keyof AggregateAttack]: P extends '_count' | 'count'
      ? T[P] extends true
        ? number
        : GetScalarType<T[P], AggregateAttack[P]>
      : GetScalarType<T[P], AggregateAttack[P]>
  }




  export type AttackGroupByArgs = {
    where?: AttackWhereInput
    orderBy?: Enumerable<AttackOrderByWithAggregationInput>
    by: AttackScalarFieldEnum[]
    having?: AttackScalarWhereWithAggregatesInput
    take?: number
    skip?: number
    _count?: AttackCountAggregateInputType | true
    _avg?: AttackAvgAggregateInputType
    _sum?: AttackSumAggregateInputType
    _min?: AttackMinAggregateInputType
    _max?: AttackMaxAggregateInputType
  }


  export type AttackGroupByOutputType = {
    name: string
    key: string
    art_key: string
    guild_id: string
    roles: string[]
    required_roles: number
    required_exp: number
    damage: number
    stamina: number
    embed_title: string | null
    embed_description: string | null
    embed_url: string | null
    fields_key: string | null
    created_at: Date
    updated_at: Date
    _count: AttackCountAggregateOutputType | null
    _avg: AttackAvgAggregateOutputType | null
    _sum: AttackSumAggregateOutputType | null
    _min: AttackMinAggregateOutputType | null
    _max: AttackMaxAggregateOutputType | null
  }

  type GetAttackGroupByPayload<T extends AttackGroupByArgs> = Prisma.PrismaPromise<
    Array<
      PickArray<AttackGroupByOutputType, T['by']> &
        {
          [P in ((keyof T) & (keyof AttackGroupByOutputType))]: P extends '_count'
            ? T[P] extends boolean
              ? number
              : GetScalarType<T[P], AttackGroupByOutputType[P]>
            : GetScalarType<T[P], AttackGroupByOutputType[P]>
        }
      >
    >


  export type AttackSelect = {
    name?: boolean
    key?: boolean
    art_key?: boolean
    guild_id?: boolean
    roles?: boolean
    required_roles?: boolean
    required_exp?: boolean
    damage?: boolean
    stamina?: boolean
    embed_title?: boolean
    embed_description?: boolean
    embed_url?: boolean
    fields_key?: boolean
    created_at?: boolean
    updated_at?: boolean
    art?: boolean | ArtArgs
  }


  export type AttackInclude = {
    art?: boolean | ArtArgs
  }

  export type AttackGetPayload<S extends boolean | null | undefined | AttackArgs> =
    S extends { select: any, include: any } ? 'Please either choose `select` or `include`' :
    S extends true ? Attack :
    S extends undefined ? never :
    S extends { include: any } & (AttackArgs | AttackFindManyArgs)
    ? Attack  & {
    [P in TruthyKeys<S['include']>]:
        P extends 'art' ? ArtGetPayload<S['include'][P]> :  never
  } 
    : S extends { select: any } & (AttackArgs | AttackFindManyArgs)
      ? {
    [P in TruthyKeys<S['select']>]:
        P extends 'art' ? ArtGetPayload<S['select'][P]> :  P extends keyof Attack ? Attack[P] : never
  } 
      : Attack


  type AttackCountArgs = 
    Omit<AttackFindManyArgs, 'select' | 'include'> & {
      select?: AttackCountAggregateInputType | true
    }

  export interface AttackDelegate<GlobalRejectSettings extends Prisma.RejectOnNotFound | Prisma.RejectPerOperation | false | undefined> {

    /**
     * Find zero or one Attack that matches the filter.
     * @param {AttackFindUniqueArgs} args - Arguments to find a Attack
     * @example
     * // Get one Attack
     * const attack = await prisma.attack.findUnique({
     *   where: {
     *     // ... provide filter here
     *   }
     * })
    **/
    findUnique<T extends AttackFindUniqueArgs,  LocalRejectSettings = T["rejectOnNotFound"] extends RejectOnNotFound ? T['rejectOnNotFound'] : undefined>(
      args: SelectSubset<T, AttackFindUniqueArgs>
    ): HasReject<GlobalRejectSettings, LocalRejectSettings, 'findUnique', 'Attack'> extends True ? Prisma__AttackClient<AttackGetPayload<T>> : Prisma__AttackClient<AttackGetPayload<T> | null, null>

    /**
     * Find one Attack that matches the filter or throw an error  with `error.code='P2025'` 
     *     if no matches were found.
     * @param {AttackFindUniqueOrThrowArgs} args - Arguments to find a Attack
     * @example
     * // Get one Attack
     * const attack = await prisma.attack.findUniqueOrThrow({
     *   where: {
     *     // ... provide filter here
     *   }
     * })
    **/
    findUniqueOrThrow<T extends AttackFindUniqueOrThrowArgs>(
      args?: SelectSubset<T, AttackFindUniqueOrThrowArgs>
    ): Prisma__AttackClient<AttackGetPayload<T>>

    /**
     * Find the first Attack that matches the filter.
     * Note, that providing `undefined` is treated as the value not being there.
     * Read more here: https://pris.ly/d/null-undefined
     * @param {AttackFindFirstArgs} args - Arguments to find a Attack
     * @example
     * // Get one Attack
     * const attack = await prisma.attack.findFirst({
     *   where: {
     *     // ... provide filter here
     *   }
     * })
    **/
    findFirst<T extends AttackFindFirstArgs,  LocalRejectSettings = T["rejectOnNotFound"] extends RejectOnNotFound ? T['rejectOnNotFound'] : undefined>(
      args?: SelectSubset<T, AttackFindFirstArgs>
    ): HasReject<GlobalRejectSettings, LocalRejectSettings, 'findFirst', 'Attack'> extends True ? Prisma__AttackClient<AttackGetPayload<T>> : Prisma__AttackClient<AttackGetPayload<T> | null, null>

    /**
     * Find the first Attack that matches the filter or
     * throw `NotFoundError` if no matches were found.
     * Note, that providing `undefined` is treated as the value not being there.
     * Read more here: https://pris.ly/d/null-undefined
     * @param {AttackFindFirstOrThrowArgs} args - Arguments to find a Attack
     * @example
     * // Get one Attack
     * const attack = await prisma.attack.findFirstOrThrow({
     *   where: {
     *     // ... provide filter here
     *   }
     * })
    **/
    findFirstOrThrow<T extends AttackFindFirstOrThrowArgs>(
      args?: SelectSubset<T, AttackFindFirstOrThrowArgs>
    ): Prisma__AttackClient<AttackGetPayload<T>>

    /**
     * Find zero or more Attacks that matches the filter.
     * Note, that providing `undefined` is treated as the value not being there.
     * Read more here: https://pris.ly/d/null-undefined
     * @param {AttackFindManyArgs=} args - Arguments to filter and select certain fields only.
     * @example
     * // Get all Attacks
     * const attacks = await prisma.attack.findMany()
     * 
     * // Get first 10 Attacks
     * const attacks = await prisma.attack.findMany({ take: 10 })
     * 
     * // Only select the `name`
     * const attackWithNameOnly = await prisma.attack.findMany({ select: { name: true } })
     * 
    **/
    findMany<T extends AttackFindManyArgs>(
      args?: SelectSubset<T, AttackFindManyArgs>
    ): Prisma.PrismaPromise<Array<AttackGetPayload<T>>>

    /**
     * Create a Attack.
     * @param {AttackCreateArgs} args - Arguments to create a Attack.
     * @example
     * // Create one Attack
     * const Attack = await prisma.attack.create({
     *   data: {
     *     // ... data to create a Attack
     *   }
     * })
     * 
    **/
    create<T extends AttackCreateArgs>(
      args: SelectSubset<T, AttackCreateArgs>
    ): Prisma__AttackClient<AttackGetPayload<T>>

    /**
     * Create many Attacks.
     *     @param {AttackCreateManyArgs} args - Arguments to create many Attacks.
     *     @example
     *     // Create many Attacks
     *     const attack = await prisma.attack.createMany({
     *       data: {
     *         // ... provide data here
     *       }
     *     })
     *     
    **/
    createMany<T extends AttackCreateManyArgs>(
      args?: SelectSubset<T, AttackCreateManyArgs>
    ): Prisma.PrismaPromise<BatchPayload>

    /**
     * Delete a Attack.
     * @param {AttackDeleteArgs} args - Arguments to delete one Attack.
     * @example
     * // Delete one Attack
     * const Attack = await prisma.attack.delete({
     *   where: {
     *     // ... filter to delete one Attack
     *   }
     * })
     * 
    **/
    delete<T extends AttackDeleteArgs>(
      args: SelectSubset<T, AttackDeleteArgs>
    ): Prisma__AttackClient<AttackGetPayload<T>>

    /**
     * Update one Attack.
     * @param {AttackUpdateArgs} args - Arguments to update one Attack.
     * @example
     * // Update one Attack
     * const attack = await prisma.attack.update({
     *   where: {
     *     // ... provide filter here
     *   },
     *   data: {
     *     // ... provide data here
     *   }
     * })
     * 
    **/
    update<T extends AttackUpdateArgs>(
      args: SelectSubset<T, AttackUpdateArgs>
    ): Prisma__AttackClient<AttackGetPayload<T>>

    /**
     * Delete zero or more Attacks.
     * @param {AttackDeleteManyArgs} args - Arguments to filter Attacks to delete.
     * @example
     * // Delete a few Attacks
     * const { count } = await prisma.attack.deleteMany({
     *   where: {
     *     // ... provide filter here
     *   }
     * })
     * 
    **/
    deleteMany<T extends AttackDeleteManyArgs>(
      args?: SelectSubset<T, AttackDeleteManyArgs>
    ): Prisma.PrismaPromise<BatchPayload>

    /**
     * Update zero or more Attacks.
     * Note, that providing `undefined` is treated as the value not being there.
     * Read more here: https://pris.ly/d/null-undefined
     * @param {AttackUpdateManyArgs} args - Arguments to update one or more rows.
     * @example
     * // Update many Attacks
     * const attack = await prisma.attack.updateMany({
     *   where: {
     *     // ... provide filter here
     *   },
     *   data: {
     *     // ... provide data here
     *   }
     * })
     * 
    **/
    updateMany<T extends AttackUpdateManyArgs>(
      args: SelectSubset<T, AttackUpdateManyArgs>
    ): Prisma.PrismaPromise<BatchPayload>

    /**
     * Create or update one Attack.
     * @param {AttackUpsertArgs} args - Arguments to update or create a Attack.
     * @example
     * // Update or create a Attack
     * const attack = await prisma.attack.upsert({
     *   create: {
     *     // ... data to create a Attack
     *   },
     *   update: {
     *     // ... in case it already exists, update
     *   },
     *   where: {
     *     // ... the filter for the Attack we want to update
     *   }
     * })
    **/
    upsert<T extends AttackUpsertArgs>(
      args: SelectSubset<T, AttackUpsertArgs>
    ): Prisma__AttackClient<AttackGetPayload<T>>

    /**
     * Count the number of Attacks.
     * Note, that providing `undefined` is treated as the value not being there.
     * Read more here: https://pris.ly/d/null-undefined
     * @param {AttackCountArgs} args - Arguments to filter Attacks to count.
     * @example
     * // Count the number of Attacks
     * const count = await prisma.attack.count({
     *   where: {
     *     // ... the filter for the Attacks we want to count
     *   }
     * })
    **/
    count<T extends AttackCountArgs>(
      args?: Subset<T, AttackCountArgs>,
    ): Prisma.PrismaPromise<
      T extends _Record<'select', any>
        ? T['select'] extends true
          ? number
          : GetScalarType<T['select'], AttackCountAggregateOutputType>
        : number
    >

    /**
     * Allows you to perform aggregations operations on a Attack.
     * Note, that providing `undefined` is treated as the value not being there.
     * Read more here: https://pris.ly/d/null-undefined
     * @param {AttackAggregateArgs} args - Select which aggregations you would like to apply and on what fields.
     * @example
     * // Ordered by age ascending
     * // Where email contains prisma.io
     * // Limited to the 10 users
     * const aggregations = await prisma.user.aggregate({
     *   _avg: {
     *     age: true,
     *   },
     *   where: {
     *     email: {
     *       contains: "prisma.io",
     *     },
     *   },
     *   orderBy: {
     *     age: "asc",
     *   },
     *   take: 10,
     * })
    **/
    aggregate<T extends AttackAggregateArgs>(args: Subset<T, AttackAggregateArgs>): Prisma.PrismaPromise<GetAttackAggregateType<T>>

    /**
     * Group by Attack.
     * Note, that providing `undefined` is treated as the value not being there.
     * Read more here: https://pris.ly/d/null-undefined
     * @param {AttackGroupByArgs} args - Group by arguments.
     * @example
     * // Group by city, order by createdAt, get count
     * const result = await prisma.user.groupBy({
     *   by: ['city', 'createdAt'],
     *   orderBy: {
     *     createdAt: true
     *   },
     *   _count: {
     *     _all: true
     *   },
     * })
     * 
    **/
    groupBy<
      T extends AttackGroupByArgs,
      HasSelectOrTake extends Or<
        Extends<'skip', Keys<T>>,
        Extends<'take', Keys<T>>
      >,
      OrderByArg extends True extends HasSelectOrTake
        ? { orderBy: AttackGroupByArgs['orderBy'] }
        : { orderBy?: AttackGroupByArgs['orderBy'] },
      OrderFields extends ExcludeUnderscoreKeys<Keys<MaybeTupleToUnion<T['orderBy']>>>,
      ByFields extends TupleToUnion<T['by']>,
      ByValid extends Has<ByFields, OrderFields>,
      HavingFields extends GetHavingFields<T['having']>,
      HavingValid extends Has<ByFields, HavingFields>,
      ByEmpty extends T['by'] extends never[] ? True : False,
      InputErrors extends ByEmpty extends True
      ? `Error: "by" must not be empty.`
      : HavingValid extends False
      ? {
          [P in HavingFields]: P extends ByFields
            ? never
            : P extends string
            ? `Error: Field "${P}" used in "having" needs to be provided in "by".`
            : [
                Error,
                'Field ',
                P,
                ` in "having" needs to be provided in "by"`,
              ]
        }[HavingFields]
      : 'take' extends Keys<T>
      ? 'orderBy' extends Keys<T>
        ? ByValid extends True
          ? {}
          : {
              [P in OrderFields]: P extends ByFields
                ? never
                : `Error: Field "${P}" in "orderBy" needs to be provided in "by"`
            }[OrderFields]
        : 'Error: If you provide "take", you also need to provide "orderBy"'
      : 'skip' extends Keys<T>
      ? 'orderBy' extends Keys<T>
        ? ByValid extends True
          ? {}
          : {
              [P in OrderFields]: P extends ByFields
                ? never
                : `Error: Field "${P}" in "orderBy" needs to be provided in "by"`
            }[OrderFields]
        : 'Error: If you provide "skip", you also need to provide "orderBy"'
      : ByValid extends True
      ? {}
      : {
          [P in OrderFields]: P extends ByFields
            ? never
            : `Error: Field "${P}" in "orderBy" needs to be provided in "by"`
        }[OrderFields]
    >(args: SubsetIntersection<T, AttackGroupByArgs, OrderByArg> & InputErrors): {} extends InputErrors ? GetAttackGroupByPayload<T> : Prisma.PrismaPromise<InputErrors>

  }

  /**
   * The delegate class that acts as a "Promise-like" for Attack.
   * Why is this prefixed with `Prisma__`?
   * Because we want to prevent naming conflicts as mentioned in
   * https://github.com/prisma/prisma-client-js/issues/707
   */
  export class Prisma__AttackClient<T, Null = never> implements Prisma.PrismaPromise<T> {
    private readonly _dmmf;
    private readonly _queryType;
    private readonly _rootField;
    private readonly _clientMethod;
    private readonly _args;
    private readonly _dataPath;
    private readonly _errorFormat;
    private readonly _measurePerformance?;
    private _isList;
    private _callsite;
    private _requestPromise?;
    readonly [Symbol.toStringTag]: 'PrismaPromise';
    constructor(_dmmf: runtime.DMMFClass, _queryType: 'query' | 'mutation', _rootField: string, _clientMethod: string, _args: any, _dataPath: string[], _errorFormat: ErrorFormat, _measurePerformance?: boolean | undefined, _isList?: boolean);

    art<T extends ArtArgs= {}>(args?: Subset<T, ArtArgs>): Prisma__ArtClient<ArtGetPayload<T> | Null>;

    private get _document();
    /**
     * Attaches callbacks for the resolution and/or rejection of the Promise.
     * @param onfulfilled The callback to execute when the Promise is resolved.
     * @param onrejected The callback to execute when the Promise is rejected.
     * @returns A Promise for the completion of which ever callback is executed.
     */
    then<TResult1 = T, TResult2 = never>(onfulfilled?: ((value: T) => TResult1 | PromiseLike<TResult1>) | undefined | null, onrejected?: ((reason: any) => TResult2 | PromiseLike<TResult2>) | undefined | null): Promise<TResult1 | TResult2>;
    /**
     * Attaches a callback for only the rejection of the Promise.
     * @param onrejected The callback to execute when the Promise is rejected.
     * @returns A Promise for the completion of the callback.
     */
    catch<TResult = never>(onrejected?: ((reason: any) => TResult | PromiseLike<TResult>) | undefined | null): Promise<T | TResult>;
    /**
     * Attaches a callback that is invoked when the Promise is settled (fulfilled or rejected). The
     * resolved value cannot be modified from the callback.
     * @param onfinally The callback to execute when the Promise is settled (fulfilled or rejected).
     * @returns A Promise for the completion of the callback.
     */
    finally(onfinally?: (() => void) | undefined | null): Promise<T>;
  }



  // Custom InputTypes

  /**
   * Attack base type for findUnique actions
   */
  export type AttackFindUniqueArgsBase = {
    /**
     * Select specific fields to fetch from the Attack
     */
    select?: AttackSelect | null
    /**
     * Choose, which related nodes to fetch as well.
     */
    include?: AttackInclude | null
    /**
     * Filter, which Attack to fetch.
     */
    where: AttackWhereUniqueInput
  }

  /**
   * Attack findUnique
   */
  export interface AttackFindUniqueArgs extends AttackFindUniqueArgsBase {
   /**
    * Throw an Error if query returns no results
    * @deprecated since 4.0.0: use `findUniqueOrThrow` method instead
    */
    rejectOnNotFound?: RejectOnNotFound
  }
      

  /**
   * Attack findUniqueOrThrow
   */
  export type AttackFindUniqueOrThrowArgs = {
    /**
     * Select specific fields to fetch from the Attack
     */
    select?: AttackSelect | null
    /**
     * Choose, which related nodes to fetch as well.
     */
    include?: AttackInclude | null
    /**
     * Filter, which Attack to fetch.
     */
    where: AttackWhereUniqueInput
  }


  /**
   * Attack base type for findFirst actions
   */
  export type AttackFindFirstArgsBase = {
    /**
     * Select specific fields to fetch from the Attack
     */
    select?: AttackSelect | null
    /**
     * Choose, which related nodes to fetch as well.
     */
    include?: AttackInclude | null
    /**
     * Filter, which Attack to fetch.
     */
    where?: AttackWhereInput
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/sorting Sorting Docs}
     * 
     * Determine the order of Attacks to fetch.
     */
    orderBy?: Enumerable<AttackOrderByWithRelationInput>
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/pagination#cursor-based-pagination Cursor Docs}
     * 
     * Sets the position for searching for Attacks.
     */
    cursor?: AttackWhereUniqueInput
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/pagination Pagination Docs}
     * 
     * Take `±n` Attacks from the position of the cursor.
     */
    take?: number
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/pagination Pagination Docs}
     * 
     * Skip the first `n` Attacks.
     */
    skip?: number
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/distinct Distinct Docs}
     * 
     * Filter by unique combinations of Attacks.
     */
    distinct?: Enumerable<AttackScalarFieldEnum>
  }

  /**
   * Attack findFirst
   */
  export interface AttackFindFirstArgs extends AttackFindFirstArgsBase {
   /**
    * Throw an Error if query returns no results
    * @deprecated since 4.0.0: use `findFirstOrThrow` method instead
    */
    rejectOnNotFound?: RejectOnNotFound
  }
      

  /**
   * Attack findFirstOrThrow
   */
  export type AttackFindFirstOrThrowArgs = {
    /**
     * Select specific fields to fetch from the Attack
     */
    select?: AttackSelect | null
    /**
     * Choose, which related nodes to fetch as well.
     */
    include?: AttackInclude | null
    /**
     * Filter, which Attack to fetch.
     */
    where?: AttackWhereInput
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/sorting Sorting Docs}
     * 
     * Determine the order of Attacks to fetch.
     */
    orderBy?: Enumerable<AttackOrderByWithRelationInput>
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/pagination#cursor-based-pagination Cursor Docs}
     * 
     * Sets the position for searching for Attacks.
     */
    cursor?: AttackWhereUniqueInput
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/pagination Pagination Docs}
     * 
     * Take `±n` Attacks from the position of the cursor.
     */
    take?: number
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/pagination Pagination Docs}
     * 
     * Skip the first `n` Attacks.
     */
    skip?: number
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/distinct Distinct Docs}
     * 
     * Filter by unique combinations of Attacks.
     */
    distinct?: Enumerable<AttackScalarFieldEnum>
  }


  /**
   * Attack findMany
   */
  export type AttackFindManyArgs = {
    /**
     * Select specific fields to fetch from the Attack
     */
    select?: AttackSelect | null
    /**
     * Choose, which related nodes to fetch as well.
     */
    include?: AttackInclude | null
    /**
     * Filter, which Attacks to fetch.
     */
    where?: AttackWhereInput
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/sorting Sorting Docs}
     * 
     * Determine the order of Attacks to fetch.
     */
    orderBy?: Enumerable<AttackOrderByWithRelationInput>
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/pagination#cursor-based-pagination Cursor Docs}
     * 
     * Sets the position for listing Attacks.
     */
    cursor?: AttackWhereUniqueInput
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/pagination Pagination Docs}
     * 
     * Take `±n` Attacks from the position of the cursor.
     */
    take?: number
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/pagination Pagination Docs}
     * 
     * Skip the first `n` Attacks.
     */
    skip?: number
    distinct?: Enumerable<AttackScalarFieldEnum>
  }


  /**
   * Attack create
   */
  export type AttackCreateArgs = {
    /**
     * Select specific fields to fetch from the Attack
     */
    select?: AttackSelect | null
    /**
     * Choose, which related nodes to fetch as well.
     */
    include?: AttackInclude | null
    /**
     * The data needed to create a Attack.
     */
    data: XOR<AttackCreateInput, AttackUncheckedCreateInput>
  }


  /**
   * Attack createMany
   */
  export type AttackCreateManyArgs = {
    /**
     * The data used to create many Attacks.
     */
    data: Enumerable<AttackCreateManyInput>
    skipDuplicates?: boolean
  }


  /**
   * Attack update
   */
  export type AttackUpdateArgs = {
    /**
     * Select specific fields to fetch from the Attack
     */
    select?: AttackSelect | null
    /**
     * Choose, which related nodes to fetch as well.
     */
    include?: AttackInclude | null
    /**
     * The data needed to update a Attack.
     */
    data: XOR<AttackUpdateInput, AttackUncheckedUpdateInput>
    /**
     * Choose, which Attack to update.
     */
    where: AttackWhereUniqueInput
  }


  /**
   * Attack updateMany
   */
  export type AttackUpdateManyArgs = {
    /**
     * The data used to update Attacks.
     */
    data: XOR<AttackUpdateManyMutationInput, AttackUncheckedUpdateManyInput>
    /**
     * Filter which Attacks to update
     */
    where?: AttackWhereInput
  }


  /**
   * Attack upsert
   */
  export type AttackUpsertArgs = {
    /**
     * Select specific fields to fetch from the Attack
     */
    select?: AttackSelect | null
    /**
     * Choose, which related nodes to fetch as well.
     */
    include?: AttackInclude | null
    /**
     * The filter to search for the Attack to update in case it exists.
     */
    where: AttackWhereUniqueInput
    /**
     * In case the Attack found by the `where` argument doesn't exist, create a new Attack with this data.
     */
    create: XOR<AttackCreateInput, AttackUncheckedCreateInput>
    /**
     * In case the Attack was found with the provided `where` argument, update it with this data.
     */
    update: XOR<AttackUpdateInput, AttackUncheckedUpdateInput>
  }


  /**
   * Attack delete
   */
  export type AttackDeleteArgs = {
    /**
     * Select specific fields to fetch from the Attack
     */
    select?: AttackSelect | null
    /**
     * Choose, which related nodes to fetch as well.
     */
    include?: AttackInclude | null
    /**
     * Filter which Attack to delete.
     */
    where: AttackWhereUniqueInput
  }


  /**
   * Attack deleteMany
   */
  export type AttackDeleteManyArgs = {
    /**
     * Filter which Attacks to delete
     */
    where?: AttackWhereInput
  }


  /**
   * Attack without action
   */
  export type AttackArgs = {
    /**
     * Select specific fields to fetch from the Attack
     */
    select?: AttackSelect | null
    /**
     * Choose, which related nodes to fetch as well.
     */
    include?: AttackInclude | null
  }



  /**
   * Model Varialble
   */


  export type AggregateVarialble = {
    _count: VarialbleCountAggregateOutputType | null
    _avg: VarialbleAvgAggregateOutputType | null
    _sum: VarialbleSumAggregateOutputType | null
    _min: VarialbleMinAggregateOutputType | null
    _max: VarialbleMaxAggregateOutputType | null
  }

  export type VarialbleAvgAggregateOutputType = {
    required_roles: number | null
  }

  export type VarialbleSumAggregateOutputType = {
    required_roles: number | null
  }

  export type VarialbleMinAggregateOutputType = {
    guild_id: string | null
    name: string | null
    text: string | null
    visibleCaseIfNotAuthorizerMember: boolean | null
    required_roles: number | null
    created_at: Date | null
    updated_at: Date | null
  }

  export type VarialbleMaxAggregateOutputType = {
    guild_id: string | null
    name: string | null
    text: string | null
    visibleCaseIfNotAuthorizerMember: boolean | null
    required_roles: number | null
    created_at: Date | null
    updated_at: Date | null
  }

  export type VarialbleCountAggregateOutputType = {
    guild_id: number
    name: number
    text: number
    visibleCaseIfNotAuthorizerMember: number
    required_roles: number
    roles: number
    created_at: number
    updated_at: number
    _all: number
  }


  export type VarialbleAvgAggregateInputType = {
    required_roles?: true
  }

  export type VarialbleSumAggregateInputType = {
    required_roles?: true
  }

  export type VarialbleMinAggregateInputType = {
    guild_id?: true
    name?: true
    text?: true
    visibleCaseIfNotAuthorizerMember?: true
    required_roles?: true
    created_at?: true
    updated_at?: true
  }

  export type VarialbleMaxAggregateInputType = {
    guild_id?: true
    name?: true
    text?: true
    visibleCaseIfNotAuthorizerMember?: true
    required_roles?: true
    created_at?: true
    updated_at?: true
  }

  export type VarialbleCountAggregateInputType = {
    guild_id?: true
    name?: true
    text?: true
    visibleCaseIfNotAuthorizerMember?: true
    required_roles?: true
    roles?: true
    created_at?: true
    updated_at?: true
    _all?: true
  }

  export type VarialbleAggregateArgs = {
    /**
     * Filter which Varialble to aggregate.
     */
    where?: VarialbleWhereInput
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/sorting Sorting Docs}
     * 
     * Determine the order of Varialbles to fetch.
     */
    orderBy?: Enumerable<VarialbleOrderByWithRelationInput>
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/pagination#cursor-based-pagination Cursor Docs}
     * 
     * Sets the start position
     */
    cursor?: VarialbleWhereUniqueInput
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/pagination Pagination Docs}
     * 
     * Take `±n` Varialbles from the position of the cursor.
     */
    take?: number
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/pagination Pagination Docs}
     * 
     * Skip the first `n` Varialbles.
     */
    skip?: number
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/aggregations Aggregation Docs}
     * 
     * Count returned Varialbles
    **/
    _count?: true | VarialbleCountAggregateInputType
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/aggregations Aggregation Docs}
     * 
     * Select which fields to average
    **/
    _avg?: VarialbleAvgAggregateInputType
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/aggregations Aggregation Docs}
     * 
     * Select which fields to sum
    **/
    _sum?: VarialbleSumAggregateInputType
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/aggregations Aggregation Docs}
     * 
     * Select which fields to find the minimum value
    **/
    _min?: VarialbleMinAggregateInputType
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/aggregations Aggregation Docs}
     * 
     * Select which fields to find the maximum value
    **/
    _max?: VarialbleMaxAggregateInputType
  }

  export type GetVarialbleAggregateType<T extends VarialbleAggregateArgs> = {
        [P in keyof T & keyof AggregateVarialble]: P extends '_count' | 'count'
      ? T[P] extends true
        ? number
        : GetScalarType<T[P], AggregateVarialble[P]>
      : GetScalarType<T[P], AggregateVarialble[P]>
  }




  export type VarialbleGroupByArgs = {
    where?: VarialbleWhereInput
    orderBy?: Enumerable<VarialbleOrderByWithAggregationInput>
    by: VarialbleScalarFieldEnum[]
    having?: VarialbleScalarWhereWithAggregatesInput
    take?: number
    skip?: number
    _count?: VarialbleCountAggregateInputType | true
    _avg?: VarialbleAvgAggregateInputType
    _sum?: VarialbleSumAggregateInputType
    _min?: VarialbleMinAggregateInputType
    _max?: VarialbleMaxAggregateInputType
  }


  export type VarialbleGroupByOutputType = {
    guild_id: string
    name: string
    text: string
    visibleCaseIfNotAuthorizerMember: boolean
    required_roles: number
    roles: string[]
    created_at: Date
    updated_at: Date
    _count: VarialbleCountAggregateOutputType | null
    _avg: VarialbleAvgAggregateOutputType | null
    _sum: VarialbleSumAggregateOutputType | null
    _min: VarialbleMinAggregateOutputType | null
    _max: VarialbleMaxAggregateOutputType | null
  }

  type GetVarialbleGroupByPayload<T extends VarialbleGroupByArgs> = Prisma.PrismaPromise<
    Array<
      PickArray<VarialbleGroupByOutputType, T['by']> &
        {
          [P in ((keyof T) & (keyof VarialbleGroupByOutputType))]: P extends '_count'
            ? T[P] extends boolean
              ? number
              : GetScalarType<T[P], VarialbleGroupByOutputType[P]>
            : GetScalarType<T[P], VarialbleGroupByOutputType[P]>
        }
      >
    >


  export type VarialbleSelect = {
    guild_id?: boolean
    name?: boolean
    text?: boolean
    visibleCaseIfNotAuthorizerMember?: boolean
    required_roles?: boolean
    roles?: boolean
    created_at?: boolean
    updated_at?: boolean
    guild?: boolean | GuildArgs
  }


  export type VarialbleInclude = {
    guild?: boolean | GuildArgs
  }

  export type VarialbleGetPayload<S extends boolean | null | undefined | VarialbleArgs> =
    S extends { select: any, include: any } ? 'Please either choose `select` or `include`' :
    S extends true ? Varialble :
    S extends undefined ? never :
    S extends { include: any } & (VarialbleArgs | VarialbleFindManyArgs)
    ? Varialble  & {
    [P in TruthyKeys<S['include']>]:
        P extends 'guild' ? GuildGetPayload<S['include'][P]> :  never
  } 
    : S extends { select: any } & (VarialbleArgs | VarialbleFindManyArgs)
      ? {
    [P in TruthyKeys<S['select']>]:
        P extends 'guild' ? GuildGetPayload<S['select'][P]> :  P extends keyof Varialble ? Varialble[P] : never
  } 
      : Varialble


  type VarialbleCountArgs = 
    Omit<VarialbleFindManyArgs, 'select' | 'include'> & {
      select?: VarialbleCountAggregateInputType | true
    }

  export interface VarialbleDelegate<GlobalRejectSettings extends Prisma.RejectOnNotFound | Prisma.RejectPerOperation | false | undefined> {

    /**
     * Find zero or one Varialble that matches the filter.
     * @param {VarialbleFindUniqueArgs} args - Arguments to find a Varialble
     * @example
     * // Get one Varialble
     * const varialble = await prisma.varialble.findUnique({
     *   where: {
     *     // ... provide filter here
     *   }
     * })
    **/
    findUnique<T extends VarialbleFindUniqueArgs,  LocalRejectSettings = T["rejectOnNotFound"] extends RejectOnNotFound ? T['rejectOnNotFound'] : undefined>(
      args: SelectSubset<T, VarialbleFindUniqueArgs>
    ): HasReject<GlobalRejectSettings, LocalRejectSettings, 'findUnique', 'Varialble'> extends True ? Prisma__VarialbleClient<VarialbleGetPayload<T>> : Prisma__VarialbleClient<VarialbleGetPayload<T> | null, null>

    /**
     * Find one Varialble that matches the filter or throw an error  with `error.code='P2025'` 
     *     if no matches were found.
     * @param {VarialbleFindUniqueOrThrowArgs} args - Arguments to find a Varialble
     * @example
     * // Get one Varialble
     * const varialble = await prisma.varialble.findUniqueOrThrow({
     *   where: {
     *     // ... provide filter here
     *   }
     * })
    **/
    findUniqueOrThrow<T extends VarialbleFindUniqueOrThrowArgs>(
      args?: SelectSubset<T, VarialbleFindUniqueOrThrowArgs>
    ): Prisma__VarialbleClient<VarialbleGetPayload<T>>

    /**
     * Find the first Varialble that matches the filter.
     * Note, that providing `undefined` is treated as the value not being there.
     * Read more here: https://pris.ly/d/null-undefined
     * @param {VarialbleFindFirstArgs} args - Arguments to find a Varialble
     * @example
     * // Get one Varialble
     * const varialble = await prisma.varialble.findFirst({
     *   where: {
     *     // ... provide filter here
     *   }
     * })
    **/
    findFirst<T extends VarialbleFindFirstArgs,  LocalRejectSettings = T["rejectOnNotFound"] extends RejectOnNotFound ? T['rejectOnNotFound'] : undefined>(
      args?: SelectSubset<T, VarialbleFindFirstArgs>
    ): HasReject<GlobalRejectSettings, LocalRejectSettings, 'findFirst', 'Varialble'> extends True ? Prisma__VarialbleClient<VarialbleGetPayload<T>> : Prisma__VarialbleClient<VarialbleGetPayload<T> | null, null>

    /**
     * Find the first Varialble that matches the filter or
     * throw `NotFoundError` if no matches were found.
     * Note, that providing `undefined` is treated as the value not being there.
     * Read more here: https://pris.ly/d/null-undefined
     * @param {VarialbleFindFirstOrThrowArgs} args - Arguments to find a Varialble
     * @example
     * // Get one Varialble
     * const varialble = await prisma.varialble.findFirstOrThrow({
     *   where: {
     *     // ... provide filter here
     *   }
     * })
    **/
    findFirstOrThrow<T extends VarialbleFindFirstOrThrowArgs>(
      args?: SelectSubset<T, VarialbleFindFirstOrThrowArgs>
    ): Prisma__VarialbleClient<VarialbleGetPayload<T>>

    /**
     * Find zero or more Varialbles that matches the filter.
     * Note, that providing `undefined` is treated as the value not being there.
     * Read more here: https://pris.ly/d/null-undefined
     * @param {VarialbleFindManyArgs=} args - Arguments to filter and select certain fields only.
     * @example
     * // Get all Varialbles
     * const varialbles = await prisma.varialble.findMany()
     * 
     * // Get first 10 Varialbles
     * const varialbles = await prisma.varialble.findMany({ take: 10 })
     * 
     * // Only select the `guild_id`
     * const varialbleWithGuild_idOnly = await prisma.varialble.findMany({ select: { guild_id: true } })
     * 
    **/
    findMany<T extends VarialbleFindManyArgs>(
      args?: SelectSubset<T, VarialbleFindManyArgs>
    ): Prisma.PrismaPromise<Array<VarialbleGetPayload<T>>>

    /**
     * Create a Varialble.
     * @param {VarialbleCreateArgs} args - Arguments to create a Varialble.
     * @example
     * // Create one Varialble
     * const Varialble = await prisma.varialble.create({
     *   data: {
     *     // ... data to create a Varialble
     *   }
     * })
     * 
    **/
    create<T extends VarialbleCreateArgs>(
      args: SelectSubset<T, VarialbleCreateArgs>
    ): Prisma__VarialbleClient<VarialbleGetPayload<T>>

    /**
     * Create many Varialbles.
     *     @param {VarialbleCreateManyArgs} args - Arguments to create many Varialbles.
     *     @example
     *     // Create many Varialbles
     *     const varialble = await prisma.varialble.createMany({
     *       data: {
     *         // ... provide data here
     *       }
     *     })
     *     
    **/
    createMany<T extends VarialbleCreateManyArgs>(
      args?: SelectSubset<T, VarialbleCreateManyArgs>
    ): Prisma.PrismaPromise<BatchPayload>

    /**
     * Delete a Varialble.
     * @param {VarialbleDeleteArgs} args - Arguments to delete one Varialble.
     * @example
     * // Delete one Varialble
     * const Varialble = await prisma.varialble.delete({
     *   where: {
     *     // ... filter to delete one Varialble
     *   }
     * })
     * 
    **/
    delete<T extends VarialbleDeleteArgs>(
      args: SelectSubset<T, VarialbleDeleteArgs>
    ): Prisma__VarialbleClient<VarialbleGetPayload<T>>

    /**
     * Update one Varialble.
     * @param {VarialbleUpdateArgs} args - Arguments to update one Varialble.
     * @example
     * // Update one Varialble
     * const varialble = await prisma.varialble.update({
     *   where: {
     *     // ... provide filter here
     *   },
     *   data: {
     *     // ... provide data here
     *   }
     * })
     * 
    **/
    update<T extends VarialbleUpdateArgs>(
      args: SelectSubset<T, VarialbleUpdateArgs>
    ): Prisma__VarialbleClient<VarialbleGetPayload<T>>

    /**
     * Delete zero or more Varialbles.
     * @param {VarialbleDeleteManyArgs} args - Arguments to filter Varialbles to delete.
     * @example
     * // Delete a few Varialbles
     * const { count } = await prisma.varialble.deleteMany({
     *   where: {
     *     // ... provide filter here
     *   }
     * })
     * 
    **/
    deleteMany<T extends VarialbleDeleteManyArgs>(
      args?: SelectSubset<T, VarialbleDeleteManyArgs>
    ): Prisma.PrismaPromise<BatchPayload>

    /**
     * Update zero or more Varialbles.
     * Note, that providing `undefined` is treated as the value not being there.
     * Read more here: https://pris.ly/d/null-undefined
     * @param {VarialbleUpdateManyArgs} args - Arguments to update one or more rows.
     * @example
     * // Update many Varialbles
     * const varialble = await prisma.varialble.updateMany({
     *   where: {
     *     // ... provide filter here
     *   },
     *   data: {
     *     // ... provide data here
     *   }
     * })
     * 
    **/
    updateMany<T extends VarialbleUpdateManyArgs>(
      args: SelectSubset<T, VarialbleUpdateManyArgs>
    ): Prisma.PrismaPromise<BatchPayload>

    /**
     * Create or update one Varialble.
     * @param {VarialbleUpsertArgs} args - Arguments to update or create a Varialble.
     * @example
     * // Update or create a Varialble
     * const varialble = await prisma.varialble.upsert({
     *   create: {
     *     // ... data to create a Varialble
     *   },
     *   update: {
     *     // ... in case it already exists, update
     *   },
     *   where: {
     *     // ... the filter for the Varialble we want to update
     *   }
     * })
    **/
    upsert<T extends VarialbleUpsertArgs>(
      args: SelectSubset<T, VarialbleUpsertArgs>
    ): Prisma__VarialbleClient<VarialbleGetPayload<T>>

    /**
     * Count the number of Varialbles.
     * Note, that providing `undefined` is treated as the value not being there.
     * Read more here: https://pris.ly/d/null-undefined
     * @param {VarialbleCountArgs} args - Arguments to filter Varialbles to count.
     * @example
     * // Count the number of Varialbles
     * const count = await prisma.varialble.count({
     *   where: {
     *     // ... the filter for the Varialbles we want to count
     *   }
     * })
    **/
    count<T extends VarialbleCountArgs>(
      args?: Subset<T, VarialbleCountArgs>,
    ): Prisma.PrismaPromise<
      T extends _Record<'select', any>
        ? T['select'] extends true
          ? number
          : GetScalarType<T['select'], VarialbleCountAggregateOutputType>
        : number
    >

    /**
     * Allows you to perform aggregations operations on a Varialble.
     * Note, that providing `undefined` is treated as the value not being there.
     * Read more here: https://pris.ly/d/null-undefined
     * @param {VarialbleAggregateArgs} args - Select which aggregations you would like to apply and on what fields.
     * @example
     * // Ordered by age ascending
     * // Where email contains prisma.io
     * // Limited to the 10 users
     * const aggregations = await prisma.user.aggregate({
     *   _avg: {
     *     age: true,
     *   },
     *   where: {
     *     email: {
     *       contains: "prisma.io",
     *     },
     *   },
     *   orderBy: {
     *     age: "asc",
     *   },
     *   take: 10,
     * })
    **/
    aggregate<T extends VarialbleAggregateArgs>(args: Subset<T, VarialbleAggregateArgs>): Prisma.PrismaPromise<GetVarialbleAggregateType<T>>

    /**
     * Group by Varialble.
     * Note, that providing `undefined` is treated as the value not being there.
     * Read more here: https://pris.ly/d/null-undefined
     * @param {VarialbleGroupByArgs} args - Group by arguments.
     * @example
     * // Group by city, order by createdAt, get count
     * const result = await prisma.user.groupBy({
     *   by: ['city', 'createdAt'],
     *   orderBy: {
     *     createdAt: true
     *   },
     *   _count: {
     *     _all: true
     *   },
     * })
     * 
    **/
    groupBy<
      T extends VarialbleGroupByArgs,
      HasSelectOrTake extends Or<
        Extends<'skip', Keys<T>>,
        Extends<'take', Keys<T>>
      >,
      OrderByArg extends True extends HasSelectOrTake
        ? { orderBy: VarialbleGroupByArgs['orderBy'] }
        : { orderBy?: VarialbleGroupByArgs['orderBy'] },
      OrderFields extends ExcludeUnderscoreKeys<Keys<MaybeTupleToUnion<T['orderBy']>>>,
      ByFields extends TupleToUnion<T['by']>,
      ByValid extends Has<ByFields, OrderFields>,
      HavingFields extends GetHavingFields<T['having']>,
      HavingValid extends Has<ByFields, HavingFields>,
      ByEmpty extends T['by'] extends never[] ? True : False,
      InputErrors extends ByEmpty extends True
      ? `Error: "by" must not be empty.`
      : HavingValid extends False
      ? {
          [P in HavingFields]: P extends ByFields
            ? never
            : P extends string
            ? `Error: Field "${P}" used in "having" needs to be provided in "by".`
            : [
                Error,
                'Field ',
                P,
                ` in "having" needs to be provided in "by"`,
              ]
        }[HavingFields]
      : 'take' extends Keys<T>
      ? 'orderBy' extends Keys<T>
        ? ByValid extends True
          ? {}
          : {
              [P in OrderFields]: P extends ByFields
                ? never
                : `Error: Field "${P}" in "orderBy" needs to be provided in "by"`
            }[OrderFields]
        : 'Error: If you provide "take", you also need to provide "orderBy"'
      : 'skip' extends Keys<T>
      ? 'orderBy' extends Keys<T>
        ? ByValid extends True
          ? {}
          : {
              [P in OrderFields]: P extends ByFields
                ? never
                : `Error: Field "${P}" in "orderBy" needs to be provided in "by"`
            }[OrderFields]
        : 'Error: If you provide "skip", you also need to provide "orderBy"'
      : ByValid extends True
      ? {}
      : {
          [P in OrderFields]: P extends ByFields
            ? never
            : `Error: Field "${P}" in "orderBy" needs to be provided in "by"`
        }[OrderFields]
    >(args: SubsetIntersection<T, VarialbleGroupByArgs, OrderByArg> & InputErrors): {} extends InputErrors ? GetVarialbleGroupByPayload<T> : Prisma.PrismaPromise<InputErrors>

  }

  /**
   * The delegate class that acts as a "Promise-like" for Varialble.
   * Why is this prefixed with `Prisma__`?
   * Because we want to prevent naming conflicts as mentioned in
   * https://github.com/prisma/prisma-client-js/issues/707
   */
  export class Prisma__VarialbleClient<T, Null = never> implements Prisma.PrismaPromise<T> {
    private readonly _dmmf;
    private readonly _queryType;
    private readonly _rootField;
    private readonly _clientMethod;
    private readonly _args;
    private readonly _dataPath;
    private readonly _errorFormat;
    private readonly _measurePerformance?;
    private _isList;
    private _callsite;
    private _requestPromise?;
    readonly [Symbol.toStringTag]: 'PrismaPromise';
    constructor(_dmmf: runtime.DMMFClass, _queryType: 'query' | 'mutation', _rootField: string, _clientMethod: string, _args: any, _dataPath: string[], _errorFormat: ErrorFormat, _measurePerformance?: boolean | undefined, _isList?: boolean);

    guild<T extends GuildArgs= {}>(args?: Subset<T, GuildArgs>): Prisma__GuildClient<GuildGetPayload<T> | Null>;

    private get _document();
    /**
     * Attaches callbacks for the resolution and/or rejection of the Promise.
     * @param onfulfilled The callback to execute when the Promise is resolved.
     * @param onrejected The callback to execute when the Promise is rejected.
     * @returns A Promise for the completion of which ever callback is executed.
     */
    then<TResult1 = T, TResult2 = never>(onfulfilled?: ((value: T) => TResult1 | PromiseLike<TResult1>) | undefined | null, onrejected?: ((reason: any) => TResult2 | PromiseLike<TResult2>) | undefined | null): Promise<TResult1 | TResult2>;
    /**
     * Attaches a callback for only the rejection of the Promise.
     * @param onrejected The callback to execute when the Promise is rejected.
     * @returns A Promise for the completion of the callback.
     */
    catch<TResult = never>(onrejected?: ((reason: any) => TResult | PromiseLike<TResult>) | undefined | null): Promise<T | TResult>;
    /**
     * Attaches a callback that is invoked when the Promise is settled (fulfilled or rejected). The
     * resolved value cannot be modified from the callback.
     * @param onfinally The callback to execute when the Promise is settled (fulfilled or rejected).
     * @returns A Promise for the completion of the callback.
     */
    finally(onfinally?: (() => void) | undefined | null): Promise<T>;
  }



  // Custom InputTypes

  /**
   * Varialble base type for findUnique actions
   */
  export type VarialbleFindUniqueArgsBase = {
    /**
     * Select specific fields to fetch from the Varialble
     */
    select?: VarialbleSelect | null
    /**
     * Choose, which related nodes to fetch as well.
     */
    include?: VarialbleInclude | null
    /**
     * Filter, which Varialble to fetch.
     */
    where: VarialbleWhereUniqueInput
  }

  /**
   * Varialble findUnique
   */
  export interface VarialbleFindUniqueArgs extends VarialbleFindUniqueArgsBase {
   /**
    * Throw an Error if query returns no results
    * @deprecated since 4.0.0: use `findUniqueOrThrow` method instead
    */
    rejectOnNotFound?: RejectOnNotFound
  }
      

  /**
   * Varialble findUniqueOrThrow
   */
  export type VarialbleFindUniqueOrThrowArgs = {
    /**
     * Select specific fields to fetch from the Varialble
     */
    select?: VarialbleSelect | null
    /**
     * Choose, which related nodes to fetch as well.
     */
    include?: VarialbleInclude | null
    /**
     * Filter, which Varialble to fetch.
     */
    where: VarialbleWhereUniqueInput
  }


  /**
   * Varialble base type for findFirst actions
   */
  export type VarialbleFindFirstArgsBase = {
    /**
     * Select specific fields to fetch from the Varialble
     */
    select?: VarialbleSelect | null
    /**
     * Choose, which related nodes to fetch as well.
     */
    include?: VarialbleInclude | null
    /**
     * Filter, which Varialble to fetch.
     */
    where?: VarialbleWhereInput
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/sorting Sorting Docs}
     * 
     * Determine the order of Varialbles to fetch.
     */
    orderBy?: Enumerable<VarialbleOrderByWithRelationInput>
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/pagination#cursor-based-pagination Cursor Docs}
     * 
     * Sets the position for searching for Varialbles.
     */
    cursor?: VarialbleWhereUniqueInput
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/pagination Pagination Docs}
     * 
     * Take `±n` Varialbles from the position of the cursor.
     */
    take?: number
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/pagination Pagination Docs}
     * 
     * Skip the first `n` Varialbles.
     */
    skip?: number
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/distinct Distinct Docs}
     * 
     * Filter by unique combinations of Varialbles.
     */
    distinct?: Enumerable<VarialbleScalarFieldEnum>
  }

  /**
   * Varialble findFirst
   */
  export interface VarialbleFindFirstArgs extends VarialbleFindFirstArgsBase {
   /**
    * Throw an Error if query returns no results
    * @deprecated since 4.0.0: use `findFirstOrThrow` method instead
    */
    rejectOnNotFound?: RejectOnNotFound
  }
      

  /**
   * Varialble findFirstOrThrow
   */
  export type VarialbleFindFirstOrThrowArgs = {
    /**
     * Select specific fields to fetch from the Varialble
     */
    select?: VarialbleSelect | null
    /**
     * Choose, which related nodes to fetch as well.
     */
    include?: VarialbleInclude | null
    /**
     * Filter, which Varialble to fetch.
     */
    where?: VarialbleWhereInput
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/sorting Sorting Docs}
     * 
     * Determine the order of Varialbles to fetch.
     */
    orderBy?: Enumerable<VarialbleOrderByWithRelationInput>
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/pagination#cursor-based-pagination Cursor Docs}
     * 
     * Sets the position for searching for Varialbles.
     */
    cursor?: VarialbleWhereUniqueInput
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/pagination Pagination Docs}
     * 
     * Take `±n` Varialbles from the position of the cursor.
     */
    take?: number
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/pagination Pagination Docs}
     * 
     * Skip the first `n` Varialbles.
     */
    skip?: number
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/distinct Distinct Docs}
     * 
     * Filter by unique combinations of Varialbles.
     */
    distinct?: Enumerable<VarialbleScalarFieldEnum>
  }


  /**
   * Varialble findMany
   */
  export type VarialbleFindManyArgs = {
    /**
     * Select specific fields to fetch from the Varialble
     */
    select?: VarialbleSelect | null
    /**
     * Choose, which related nodes to fetch as well.
     */
    include?: VarialbleInclude | null
    /**
     * Filter, which Varialbles to fetch.
     */
    where?: VarialbleWhereInput
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/sorting Sorting Docs}
     * 
     * Determine the order of Varialbles to fetch.
     */
    orderBy?: Enumerable<VarialbleOrderByWithRelationInput>
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/pagination#cursor-based-pagination Cursor Docs}
     * 
     * Sets the position for listing Varialbles.
     */
    cursor?: VarialbleWhereUniqueInput
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/pagination Pagination Docs}
     * 
     * Take `±n` Varialbles from the position of the cursor.
     */
    take?: number
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/pagination Pagination Docs}
     * 
     * Skip the first `n` Varialbles.
     */
    skip?: number
    distinct?: Enumerable<VarialbleScalarFieldEnum>
  }


  /**
   * Varialble create
   */
  export type VarialbleCreateArgs = {
    /**
     * Select specific fields to fetch from the Varialble
     */
    select?: VarialbleSelect | null
    /**
     * Choose, which related nodes to fetch as well.
     */
    include?: VarialbleInclude | null
    /**
     * The data needed to create a Varialble.
     */
    data: XOR<VarialbleCreateInput, VarialbleUncheckedCreateInput>
  }


  /**
   * Varialble createMany
   */
  export type VarialbleCreateManyArgs = {
    /**
     * The data used to create many Varialbles.
     */
    data: Enumerable<VarialbleCreateManyInput>
    skipDuplicates?: boolean
  }


  /**
   * Varialble update
   */
  export type VarialbleUpdateArgs = {
    /**
     * Select specific fields to fetch from the Varialble
     */
    select?: VarialbleSelect | null
    /**
     * Choose, which related nodes to fetch as well.
     */
    include?: VarialbleInclude | null
    /**
     * The data needed to update a Varialble.
     */
    data: XOR<VarialbleUpdateInput, VarialbleUncheckedUpdateInput>
    /**
     * Choose, which Varialble to update.
     */
    where: VarialbleWhereUniqueInput
  }


  /**
   * Varialble updateMany
   */
  export type VarialbleUpdateManyArgs = {
    /**
     * The data used to update Varialbles.
     */
    data: XOR<VarialbleUpdateManyMutationInput, VarialbleUncheckedUpdateManyInput>
    /**
     * Filter which Varialbles to update
     */
    where?: VarialbleWhereInput
  }


  /**
   * Varialble upsert
   */
  export type VarialbleUpsertArgs = {
    /**
     * Select specific fields to fetch from the Varialble
     */
    select?: VarialbleSelect | null
    /**
     * Choose, which related nodes to fetch as well.
     */
    include?: VarialbleInclude | null
    /**
     * The filter to search for the Varialble to update in case it exists.
     */
    where: VarialbleWhereUniqueInput
    /**
     * In case the Varialble found by the `where` argument doesn't exist, create a new Varialble with this data.
     */
    create: XOR<VarialbleCreateInput, VarialbleUncheckedCreateInput>
    /**
     * In case the Varialble was found with the provided `where` argument, update it with this data.
     */
    update: XOR<VarialbleUpdateInput, VarialbleUncheckedUpdateInput>
  }


  /**
   * Varialble delete
   */
  export type VarialbleDeleteArgs = {
    /**
     * Select specific fields to fetch from the Varialble
     */
    select?: VarialbleSelect | null
    /**
     * Choose, which related nodes to fetch as well.
     */
    include?: VarialbleInclude | null
    /**
     * Filter which Varialble to delete.
     */
    where: VarialbleWhereUniqueInput
  }


  /**
   * Varialble deleteMany
   */
  export type VarialbleDeleteManyArgs = {
    /**
     * Filter which Varialbles to delete
     */
    where?: VarialbleWhereInput
  }


  /**
   * Varialble without action
   */
  export type VarialbleArgs = {
    /**
     * Select specific fields to fetch from the Varialble
     */
    select?: VarialbleSelect | null
    /**
     * Choose, which related nodes to fetch as well.
     */
    include?: VarialbleInclude | null
  }



  /**
   * Enums
   */

  export const ArtScalarFieldEnum: {
    name: 'name',
    key: 'key',
    type: 'type',
    role: 'role',
    guild_id: 'guild_id',
    embed_title: 'embed_title',
    embed_description: 'embed_description',
    embed_url: 'embed_url',
    created_at: 'created_at',
    updated_at: 'updated_at'
  };

  export type ArtScalarFieldEnum = (typeof ArtScalarFieldEnum)[keyof typeof ArtScalarFieldEnum]


  export const AttackScalarFieldEnum: {
    name: 'name',
    key: 'key',
    art_key: 'art_key',
    guild_id: 'guild_id',
    roles: 'roles',
    required_roles: 'required_roles',
    required_exp: 'required_exp',
    damage: 'damage',
    stamina: 'stamina',
    embed_title: 'embed_title',
    embed_description: 'embed_description',
    embed_url: 'embed_url',
    fields_key: 'fields_key',
    created_at: 'created_at',
    updated_at: 'updated_at'
  };

  export type AttackScalarFieldEnum = (typeof AttackScalarFieldEnum)[keyof typeof AttackScalarFieldEnum]


  export const GuildScalarFieldEnum: {
    id: 'id',
    created_at: 'created_at',
    updated_at: 'updated_at'
  };

  export type GuildScalarFieldEnum = (typeof GuildScalarFieldEnum)[keyof typeof GuildScalarFieldEnum]


  export const QueryMode: {
    default: 'default',
    insensitive: 'insensitive'
  };

  export type QueryMode = (typeof QueryMode)[keyof typeof QueryMode]


  export const SortOrder: {
    asc: 'asc',
    desc: 'desc'
  };

  export type SortOrder = (typeof SortOrder)[keyof typeof SortOrder]


  export const TransactionIsolationLevel: {
    ReadUncommitted: 'ReadUncommitted',
    ReadCommitted: 'ReadCommitted',
    RepeatableRead: 'RepeatableRead',
    Serializable: 'Serializable'
  };

  export type TransactionIsolationLevel = (typeof TransactionIsolationLevel)[keyof typeof TransactionIsolationLevel]


  export const VarialbleScalarFieldEnum: {
    guild_id: 'guild_id',
    name: 'name',
    text: 'text',
    visibleCaseIfNotAuthorizerMember: 'visibleCaseIfNotAuthorizerMember',
    required_roles: 'required_roles',
    roles: 'roles',
    created_at: 'created_at',
    updated_at: 'updated_at'
  };

  export type VarialbleScalarFieldEnum = (typeof VarialbleScalarFieldEnum)[keyof typeof VarialbleScalarFieldEnum]


  /**
   * Deep Input Types
   */


  export type GuildWhereInput = {
    AND?: Enumerable<GuildWhereInput>
    OR?: Enumerable<GuildWhereInput>
    NOT?: Enumerable<GuildWhereInput>
    id?: StringFilter | string
    created_at?: DateTimeFilter | Date | string
    updated_at?: DateTimeFilter | Date | string
    arts?: ArtListRelationFilter
    vars?: VarialbleListRelationFilter
  }

  export type GuildOrderByWithRelationInput = {
    id?: SortOrder
    created_at?: SortOrder
    updated_at?: SortOrder
    arts?: ArtOrderByRelationAggregateInput
    vars?: VarialbleOrderByRelationAggregateInput
  }

  export type GuildWhereUniqueInput = {
    id?: string
  }

  export type GuildOrderByWithAggregationInput = {
    id?: SortOrder
    created_at?: SortOrder
    updated_at?: SortOrder
    _count?: GuildCountOrderByAggregateInput
    _max?: GuildMaxOrderByAggregateInput
    _min?: GuildMinOrderByAggregateInput
  }

  export type GuildScalarWhereWithAggregatesInput = {
    AND?: Enumerable<GuildScalarWhereWithAggregatesInput>
    OR?: Enumerable<GuildScalarWhereWithAggregatesInput>
    NOT?: Enumerable<GuildScalarWhereWithAggregatesInput>
    id?: StringWithAggregatesFilter | string
    created_at?: DateTimeWithAggregatesFilter | Date | string
    updated_at?: DateTimeWithAggregatesFilter | Date | string
  }

  export type ArtWhereInput = {
    AND?: Enumerable<ArtWhereInput>
    OR?: Enumerable<ArtWhereInput>
    NOT?: Enumerable<ArtWhereInput>
    name?: StringFilter | string
    key?: StringFilter | string
    type?: EnumArtTypeFilter | ArtType
    role?: StringNullableFilter | string | null
    guild_id?: StringFilter | string
    embed_title?: StringNullableFilter | string | null
    embed_description?: StringNullableFilter | string | null
    embed_url?: StringNullableFilter | string | null
    created_at?: DateTimeFilter | Date | string
    updated_at?: DateTimeFilter | Date | string
    guild?: XOR<GuildRelationFilter, GuildWhereInput>
    attacks?: AttackListRelationFilter
  }

  export type ArtOrderByWithRelationInput = {
    name?: SortOrder
    key?: SortOrder
    type?: SortOrder
    role?: SortOrder
    guild_id?: SortOrder
    embed_title?: SortOrder
    embed_description?: SortOrder
    embed_url?: SortOrder
    created_at?: SortOrder
    updated_at?: SortOrder
    guild?: GuildOrderByWithRelationInput
    attacks?: AttackOrderByRelationAggregateInput
  }

  export type ArtWhereUniqueInput = {
    key_guild_id?: ArtKeyGuild_idCompoundUniqueInput
  }

  export type ArtOrderByWithAggregationInput = {
    name?: SortOrder
    key?: SortOrder
    type?: SortOrder
    role?: SortOrder
    guild_id?: SortOrder
    embed_title?: SortOrder
    embed_description?: SortOrder
    embed_url?: SortOrder
    created_at?: SortOrder
    updated_at?: SortOrder
    _count?: ArtCountOrderByAggregateInput
    _max?: ArtMaxOrderByAggregateInput
    _min?: ArtMinOrderByAggregateInput
  }

  export type ArtScalarWhereWithAggregatesInput = {
    AND?: Enumerable<ArtScalarWhereWithAggregatesInput>
    OR?: Enumerable<ArtScalarWhereWithAggregatesInput>
    NOT?: Enumerable<ArtScalarWhereWithAggregatesInput>
    name?: StringWithAggregatesFilter | string
    key?: StringWithAggregatesFilter | string
    type?: EnumArtTypeWithAggregatesFilter | ArtType
    role?: StringNullableWithAggregatesFilter | string | null
    guild_id?: StringWithAggregatesFilter | string
    embed_title?: StringNullableWithAggregatesFilter | string | null
    embed_description?: StringNullableWithAggregatesFilter | string | null
    embed_url?: StringNullableWithAggregatesFilter | string | null
    created_at?: DateTimeWithAggregatesFilter | Date | string
    updated_at?: DateTimeWithAggregatesFilter | Date | string
  }

  export type AttackWhereInput = {
    AND?: Enumerable<AttackWhereInput>
    OR?: Enumerable<AttackWhereInput>
    NOT?: Enumerable<AttackWhereInput>
    name?: StringFilter | string
    key?: StringFilter | string
    art_key?: StringFilter | string
    guild_id?: StringFilter | string
    roles?: StringNullableListFilter
    required_roles?: IntFilter | number
    required_exp?: IntFilter | number
    damage?: IntFilter | number
    stamina?: IntFilter | number
    embed_title?: StringNullableFilter | string | null
    embed_description?: StringNullableFilter | string | null
    embed_url?: StringNullableFilter | string | null
    fields_key?: StringNullableFilter | string | null
    created_at?: DateTimeFilter | Date | string
    updated_at?: DateTimeFilter | Date | string
    art?: XOR<ArtRelationFilter, ArtWhereInput>
  }

  export type AttackOrderByWithRelationInput = {
    name?: SortOrder
    key?: SortOrder
    art_key?: SortOrder
    guild_id?: SortOrder
    roles?: SortOrder
    required_roles?: SortOrder
    required_exp?: SortOrder
    damage?: SortOrder
    stamina?: SortOrder
    embed_title?: SortOrder
    embed_description?: SortOrder
    embed_url?: SortOrder
    fields_key?: SortOrder
    created_at?: SortOrder
    updated_at?: SortOrder
    art?: ArtOrderByWithRelationInput
  }

  export type AttackWhereUniqueInput = {
    key_guild_id?: AttackKeyGuild_idCompoundUniqueInput
  }

  export type AttackOrderByWithAggregationInput = {
    name?: SortOrder
    key?: SortOrder
    art_key?: SortOrder
    guild_id?: SortOrder
    roles?: SortOrder
    required_roles?: SortOrder
    required_exp?: SortOrder
    damage?: SortOrder
    stamina?: SortOrder
    embed_title?: SortOrder
    embed_description?: SortOrder
    embed_url?: SortOrder
    fields_key?: SortOrder
    created_at?: SortOrder
    updated_at?: SortOrder
    _count?: AttackCountOrderByAggregateInput
    _avg?: AttackAvgOrderByAggregateInput
    _max?: AttackMaxOrderByAggregateInput
    _min?: AttackMinOrderByAggregateInput
    _sum?: AttackSumOrderByAggregateInput
  }

  export type AttackScalarWhereWithAggregatesInput = {
    AND?: Enumerable<AttackScalarWhereWithAggregatesInput>
    OR?: Enumerable<AttackScalarWhereWithAggregatesInput>
    NOT?: Enumerable<AttackScalarWhereWithAggregatesInput>
    name?: StringWithAggregatesFilter | string
    key?: StringWithAggregatesFilter | string
    art_key?: StringWithAggregatesFilter | string
    guild_id?: StringWithAggregatesFilter | string
    roles?: StringNullableListFilter
    required_roles?: IntWithAggregatesFilter | number
    required_exp?: IntWithAggregatesFilter | number
    damage?: IntWithAggregatesFilter | number
    stamina?: IntWithAggregatesFilter | number
    embed_title?: StringNullableWithAggregatesFilter | string | null
    embed_description?: StringNullableWithAggregatesFilter | string | null
    embed_url?: StringNullableWithAggregatesFilter | string | null
    fields_key?: StringNullableWithAggregatesFilter | string | null
    created_at?: DateTimeWithAggregatesFilter | Date | string
    updated_at?: DateTimeWithAggregatesFilter | Date | string
  }

  export type VarialbleWhereInput = {
    AND?: Enumerable<VarialbleWhereInput>
    OR?: Enumerable<VarialbleWhereInput>
    NOT?: Enumerable<VarialbleWhereInput>
    guild_id?: StringFilter | string
    name?: StringFilter | string
    text?: StringFilter | string
    visibleCaseIfNotAuthorizerMember?: BoolFilter | boolean
    required_roles?: IntFilter | number
    roles?: StringNullableListFilter
    created_at?: DateTimeFilter | Date | string
    updated_at?: DateTimeFilter | Date | string
    guild?: XOR<GuildRelationFilter, GuildWhereInput>
  }

  export type VarialbleOrderByWithRelationInput = {
    guild_id?: SortOrder
    name?: SortOrder
    text?: SortOrder
    visibleCaseIfNotAuthorizerMember?: SortOrder
    required_roles?: SortOrder
    roles?: SortOrder
    created_at?: SortOrder
    updated_at?: SortOrder
    guild?: GuildOrderByWithRelationInput
  }

  export type VarialbleWhereUniqueInput = {
    guild_id_name?: VarialbleGuild_idNameCompoundUniqueInput
  }

  export type VarialbleOrderByWithAggregationInput = {
    guild_id?: SortOrder
    name?: SortOrder
    text?: SortOrder
    visibleCaseIfNotAuthorizerMember?: SortOrder
    required_roles?: SortOrder
    roles?: SortOrder
    created_at?: SortOrder
    updated_at?: SortOrder
    _count?: VarialbleCountOrderByAggregateInput
    _avg?: VarialbleAvgOrderByAggregateInput
    _max?: VarialbleMaxOrderByAggregateInput
    _min?: VarialbleMinOrderByAggregateInput
    _sum?: VarialbleSumOrderByAggregateInput
  }

  export type VarialbleScalarWhereWithAggregatesInput = {
    AND?: Enumerable<VarialbleScalarWhereWithAggregatesInput>
    OR?: Enumerable<VarialbleScalarWhereWithAggregatesInput>
    NOT?: Enumerable<VarialbleScalarWhereWithAggregatesInput>
    guild_id?: StringWithAggregatesFilter | string
    name?: StringWithAggregatesFilter | string
    text?: StringWithAggregatesFilter | string
    visibleCaseIfNotAuthorizerMember?: BoolWithAggregatesFilter | boolean
    required_roles?: IntWithAggregatesFilter | number
    roles?: StringNullableListFilter
    created_at?: DateTimeWithAggregatesFilter | Date | string
    updated_at?: DateTimeWithAggregatesFilter | Date | string
  }

  export type GuildCreateInput = {
    id: string
    created_at?: Date | string
    updated_at?: Date | string
    arts?: ArtCreateNestedManyWithoutGuildInput
    vars?: VarialbleCreateNestedManyWithoutGuildInput
  }

  export type GuildUncheckedCreateInput = {
    id: string
    created_at?: Date | string
    updated_at?: Date | string
    arts?: ArtUncheckedCreateNestedManyWithoutGuildInput
    vars?: VarialbleUncheckedCreateNestedManyWithoutGuildInput
  }

  export type GuildUpdateInput = {
    id?: StringFieldUpdateOperationsInput | string
    created_at?: DateTimeFieldUpdateOperationsInput | Date | string
    updated_at?: DateTimeFieldUpdateOperationsInput | Date | string
    arts?: ArtUpdateManyWithoutGuildNestedInput
    vars?: VarialbleUpdateManyWithoutGuildNestedInput
  }

  export type GuildUncheckedUpdateInput = {
    id?: StringFieldUpdateOperationsInput | string
    created_at?: DateTimeFieldUpdateOperationsInput | Date | string
    updated_at?: DateTimeFieldUpdateOperationsInput | Date | string
    arts?: ArtUncheckedUpdateManyWithoutGuildNestedInput
    vars?: VarialbleUncheckedUpdateManyWithoutGuildNestedInput
  }

  export type GuildCreateManyInput = {
    id: string
    created_at?: Date | string
    updated_at?: Date | string
  }

  export type GuildUpdateManyMutationInput = {
    id?: StringFieldUpdateOperationsInput | string
    created_at?: DateTimeFieldUpdateOperationsInput | Date | string
    updated_at?: DateTimeFieldUpdateOperationsInput | Date | string
  }

  export type GuildUncheckedUpdateManyInput = {
    id?: StringFieldUpdateOperationsInput | string
    created_at?: DateTimeFieldUpdateOperationsInput | Date | string
    updated_at?: DateTimeFieldUpdateOperationsInput | Date | string
  }

  export type ArtCreateInput = {
    name: string
    key: string
    type: ArtType
    role?: string | null
    embed_title?: string | null
    embed_description?: string | null
    embed_url?: string | null
    created_at?: Date | string
    updated_at?: Date | string
    guild: GuildCreateNestedOneWithoutArtsInput
    attacks?: AttackCreateNestedManyWithoutArtInput
  }

  export type ArtUncheckedCreateInput = {
    name: string
    key: string
    type: ArtType
    role?: string | null
    guild_id: string
    embed_title?: string | null
    embed_description?: string | null
    embed_url?: string | null
    created_at?: Date | string
    updated_at?: Date | string
    attacks?: AttackUncheckedCreateNestedManyWithoutArtInput
  }

  export type ArtUpdateInput = {
    name?: StringFieldUpdateOperationsInput | string
    key?: StringFieldUpdateOperationsInput | string
    type?: EnumArtTypeFieldUpdateOperationsInput | ArtType
    role?: NullableStringFieldUpdateOperationsInput | string | null
    embed_title?: NullableStringFieldUpdateOperationsInput | string | null
    embed_description?: NullableStringFieldUpdateOperationsInput | string | null
    embed_url?: NullableStringFieldUpdateOperationsInput | string | null
    created_at?: DateTimeFieldUpdateOperationsInput | Date | string
    updated_at?: DateTimeFieldUpdateOperationsInput | Date | string
    guild?: GuildUpdateOneRequiredWithoutArtsNestedInput
    attacks?: AttackUpdateManyWithoutArtNestedInput
  }

  export type ArtUncheckedUpdateInput = {
    name?: StringFieldUpdateOperationsInput | string
    key?: StringFieldUpdateOperationsInput | string
    type?: EnumArtTypeFieldUpdateOperationsInput | ArtType
    role?: NullableStringFieldUpdateOperationsInput | string | null
    guild_id?: StringFieldUpdateOperationsInput | string
    embed_title?: NullableStringFieldUpdateOperationsInput | string | null
    embed_description?: NullableStringFieldUpdateOperationsInput | string | null
    embed_url?: NullableStringFieldUpdateOperationsInput | string | null
    created_at?: DateTimeFieldUpdateOperationsInput | Date | string
    updated_at?: DateTimeFieldUpdateOperationsInput | Date | string
    attacks?: AttackUncheckedUpdateManyWithoutArtNestedInput
  }

  export type ArtCreateManyInput = {
    name: string
    key: string
    type: ArtType
    role?: string | null
    guild_id: string
    embed_title?: string | null
    embed_description?: string | null
    embed_url?: string | null
    created_at?: Date | string
    updated_at?: Date | string
  }

  export type ArtUpdateManyMutationInput = {
    name?: StringFieldUpdateOperationsInput | string
    key?: StringFieldUpdateOperationsInput | string
    type?: EnumArtTypeFieldUpdateOperationsInput | ArtType
    role?: NullableStringFieldUpdateOperationsInput | string | null
    embed_title?: NullableStringFieldUpdateOperationsInput | string | null
    embed_description?: NullableStringFieldUpdateOperationsInput | string | null
    embed_url?: NullableStringFieldUpdateOperationsInput | string | null
    created_at?: DateTimeFieldUpdateOperationsInput | Date | string
    updated_at?: DateTimeFieldUpdateOperationsInput | Date | string
  }

  export type ArtUncheckedUpdateManyInput = {
    name?: StringFieldUpdateOperationsInput | string
    key?: StringFieldUpdateOperationsInput | string
    type?: EnumArtTypeFieldUpdateOperationsInput | ArtType
    role?: NullableStringFieldUpdateOperationsInput | string | null
    guild_id?: StringFieldUpdateOperationsInput | string
    embed_title?: NullableStringFieldUpdateOperationsInput | string | null
    embed_description?: NullableStringFieldUpdateOperationsInput | string | null
    embed_url?: NullableStringFieldUpdateOperationsInput | string | null
    created_at?: DateTimeFieldUpdateOperationsInput | Date | string
    updated_at?: DateTimeFieldUpdateOperationsInput | Date | string
  }

  export type AttackCreateInput = {
    name: string
    key: string
    roles?: AttackCreaterolesInput | Enumerable<string>
    required_roles?: number
    required_exp?: number
    damage?: number
    stamina?: number
    embed_title?: string | null
    embed_description?: string | null
    embed_url?: string | null
    fields_key?: string | null
    created_at?: Date | string
    updated_at?: Date | string
    art: ArtCreateNestedOneWithoutAttacksInput
  }

  export type AttackUncheckedCreateInput = {
    name: string
    key: string
    art_key: string
    guild_id: string
    roles?: AttackCreaterolesInput | Enumerable<string>
    required_roles?: number
    required_exp?: number
    damage?: number
    stamina?: number
    embed_title?: string | null
    embed_description?: string | null
    embed_url?: string | null
    fields_key?: string | null
    created_at?: Date | string
    updated_at?: Date | string
  }

  export type AttackUpdateInput = {
    name?: StringFieldUpdateOperationsInput | string
    key?: StringFieldUpdateOperationsInput | string
    roles?: AttackUpdaterolesInput | Enumerable<string>
    required_roles?: IntFieldUpdateOperationsInput | number
    required_exp?: IntFieldUpdateOperationsInput | number
    damage?: IntFieldUpdateOperationsInput | number
    stamina?: IntFieldUpdateOperationsInput | number
    embed_title?: NullableStringFieldUpdateOperationsInput | string | null
    embed_description?: NullableStringFieldUpdateOperationsInput | string | null
    embed_url?: NullableStringFieldUpdateOperationsInput | string | null
    fields_key?: NullableStringFieldUpdateOperationsInput | string | null
    created_at?: DateTimeFieldUpdateOperationsInput | Date | string
    updated_at?: DateTimeFieldUpdateOperationsInput | Date | string
    art?: ArtUpdateOneRequiredWithoutAttacksNestedInput
  }

  export type AttackUncheckedUpdateInput = {
    name?: StringFieldUpdateOperationsInput | string
    key?: StringFieldUpdateOperationsInput | string
    art_key?: StringFieldUpdateOperationsInput | string
    guild_id?: StringFieldUpdateOperationsInput | string
    roles?: AttackUpdaterolesInput | Enumerable<string>
    required_roles?: IntFieldUpdateOperationsInput | number
    required_exp?: IntFieldUpdateOperationsInput | number
    damage?: IntFieldUpdateOperationsInput | number
    stamina?: IntFieldUpdateOperationsInput | number
    embed_title?: NullableStringFieldUpdateOperationsInput | string | null
    embed_description?: NullableStringFieldUpdateOperationsInput | string | null
    embed_url?: NullableStringFieldUpdateOperationsInput | string | null
    fields_key?: NullableStringFieldUpdateOperationsInput | string | null
    created_at?: DateTimeFieldUpdateOperationsInput | Date | string
    updated_at?: DateTimeFieldUpdateOperationsInput | Date | string
  }

  export type AttackCreateManyInput = {
    name: string
    key: string
    art_key: string
    guild_id: string
    roles?: AttackCreaterolesInput | Enumerable<string>
    required_roles?: number
    required_exp?: number
    damage?: number
    stamina?: number
    embed_title?: string | null
    embed_description?: string | null
    embed_url?: string | null
    fields_key?: string | null
    created_at?: Date | string
    updated_at?: Date | string
  }

  export type AttackUpdateManyMutationInput = {
    name?: StringFieldUpdateOperationsInput | string
    key?: StringFieldUpdateOperationsInput | string
    roles?: AttackUpdaterolesInput | Enumerable<string>
    required_roles?: IntFieldUpdateOperationsInput | number
    required_exp?: IntFieldUpdateOperationsInput | number
    damage?: IntFieldUpdateOperationsInput | number
    stamina?: IntFieldUpdateOperationsInput | number
    embed_title?: NullableStringFieldUpdateOperationsInput | string | null
    embed_description?: NullableStringFieldUpdateOperationsInput | string | null
    embed_url?: NullableStringFieldUpdateOperationsInput | string | null
    fields_key?: NullableStringFieldUpdateOperationsInput | string | null
    created_at?: DateTimeFieldUpdateOperationsInput | Date | string
    updated_at?: DateTimeFieldUpdateOperationsInput | Date | string
  }

  export type AttackUncheckedUpdateManyInput = {
    name?: StringFieldUpdateOperationsInput | string
    key?: StringFieldUpdateOperationsInput | string
    art_key?: StringFieldUpdateOperationsInput | string
    guild_id?: StringFieldUpdateOperationsInput | string
    roles?: AttackUpdaterolesInput | Enumerable<string>
    required_roles?: IntFieldUpdateOperationsInput | number
    required_exp?: IntFieldUpdateOperationsInput | number
    damage?: IntFieldUpdateOperationsInput | number
    stamina?: IntFieldUpdateOperationsInput | number
    embed_title?: NullableStringFieldUpdateOperationsInput | string | null
    embed_description?: NullableStringFieldUpdateOperationsInput | string | null
    embed_url?: NullableStringFieldUpdateOperationsInput | string | null
    fields_key?: NullableStringFieldUpdateOperationsInput | string | null
    created_at?: DateTimeFieldUpdateOperationsInput | Date | string
    updated_at?: DateTimeFieldUpdateOperationsInput | Date | string
  }

  export type VarialbleCreateInput = {
    name: string
    text: string
    visibleCaseIfNotAuthorizerMember?: boolean
    required_roles?: number
    roles?: VarialbleCreaterolesInput | Enumerable<string>
    created_at?: Date | string
    updated_at?: Date | string
    guild: GuildCreateNestedOneWithoutVarsInput
  }

  export type VarialbleUncheckedCreateInput = {
    guild_id: string
    name: string
    text: string
    visibleCaseIfNotAuthorizerMember?: boolean
    required_roles?: number
    roles?: VarialbleCreaterolesInput | Enumerable<string>
    created_at?: Date | string
    updated_at?: Date | string
  }

  export type VarialbleUpdateInput = {
    name?: StringFieldUpdateOperationsInput | string
    text?: StringFieldUpdateOperationsInput | string
    visibleCaseIfNotAuthorizerMember?: BoolFieldUpdateOperationsInput | boolean
    required_roles?: IntFieldUpdateOperationsInput | number
    roles?: VarialbleUpdaterolesInput | Enumerable<string>
    created_at?: DateTimeFieldUpdateOperationsInput | Date | string
    updated_at?: DateTimeFieldUpdateOperationsInput | Date | string
    guild?: GuildUpdateOneRequiredWithoutVarsNestedInput
  }

  export type VarialbleUncheckedUpdateInput = {
    guild_id?: StringFieldUpdateOperationsInput | string
    name?: StringFieldUpdateOperationsInput | string
    text?: StringFieldUpdateOperationsInput | string
    visibleCaseIfNotAuthorizerMember?: BoolFieldUpdateOperationsInput | boolean
    required_roles?: IntFieldUpdateOperationsInput | number
    roles?: VarialbleUpdaterolesInput | Enumerable<string>
    created_at?: DateTimeFieldUpdateOperationsInput | Date | string
    updated_at?: DateTimeFieldUpdateOperationsInput | Date | string
  }

  export type VarialbleCreateManyInput = {
    guild_id: string
    name: string
    text: string
    visibleCaseIfNotAuthorizerMember?: boolean
    required_roles?: number
    roles?: VarialbleCreaterolesInput | Enumerable<string>
    created_at?: Date | string
    updated_at?: Date | string
  }

  export type VarialbleUpdateManyMutationInput = {
    name?: StringFieldUpdateOperationsInput | string
    text?: StringFieldUpdateOperationsInput | string
    visibleCaseIfNotAuthorizerMember?: BoolFieldUpdateOperationsInput | boolean
    required_roles?: IntFieldUpdateOperationsInput | number
    roles?: VarialbleUpdaterolesInput | Enumerable<string>
    created_at?: DateTimeFieldUpdateOperationsInput | Date | string
    updated_at?: DateTimeFieldUpdateOperationsInput | Date | string
  }

  export type VarialbleUncheckedUpdateManyInput = {
    guild_id?: StringFieldUpdateOperationsInput | string
    name?: StringFieldUpdateOperationsInput | string
    text?: StringFieldUpdateOperationsInput | string
    visibleCaseIfNotAuthorizerMember?: BoolFieldUpdateOperationsInput | boolean
    required_roles?: IntFieldUpdateOperationsInput | number
    roles?: VarialbleUpdaterolesInput | Enumerable<string>
    created_at?: DateTimeFieldUpdateOperationsInput | Date | string
    updated_at?: DateTimeFieldUpdateOperationsInput | Date | string
  }

  export type StringFilter = {
    equals?: string
    in?: Enumerable<string> | string
    notIn?: Enumerable<string> | string
    lt?: string
    lte?: string
    gt?: string
    gte?: string
    contains?: string
    startsWith?: string
    endsWith?: string
    mode?: QueryMode
    not?: NestedStringFilter | string
  }

  export type DateTimeFilter = {
    equals?: Date | string
    in?: Enumerable<Date> | Enumerable<string> | Date | string
    notIn?: Enumerable<Date> | Enumerable<string> | Date | string
    lt?: Date | string
    lte?: Date | string
    gt?: Date | string
    gte?: Date | string
    not?: NestedDateTimeFilter | Date | string
  }

  export type ArtListRelationFilter = {
    every?: ArtWhereInput
    some?: ArtWhereInput
    none?: ArtWhereInput
  }

  export type VarialbleListRelationFilter = {
    every?: VarialbleWhereInput
    some?: VarialbleWhereInput
    none?: VarialbleWhereInput
  }

  export type ArtOrderByRelationAggregateInput = {
    _count?: SortOrder
  }

  export type VarialbleOrderByRelationAggregateInput = {
    _count?: SortOrder
  }

  export type GuildCountOrderByAggregateInput = {
    id?: SortOrder
    created_at?: SortOrder
    updated_at?: SortOrder
  }

  export type GuildMaxOrderByAggregateInput = {
    id?: SortOrder
    created_at?: SortOrder
    updated_at?: SortOrder
  }

  export type GuildMinOrderByAggregateInput = {
    id?: SortOrder
    created_at?: SortOrder
    updated_at?: SortOrder
  }

  export type StringWithAggregatesFilter = {
    equals?: string
    in?: Enumerable<string> | string
    notIn?: Enumerable<string> | string
    lt?: string
    lte?: string
    gt?: string
    gte?: string
    contains?: string
    startsWith?: string
    endsWith?: string
    mode?: QueryMode
    not?: NestedStringWithAggregatesFilter | string
    _count?: NestedIntFilter
    _min?: NestedStringFilter
    _max?: NestedStringFilter
  }

  export type DateTimeWithAggregatesFilter = {
    equals?: Date | string
    in?: Enumerable<Date> | Enumerable<string> | Date | string
    notIn?: Enumerable<Date> | Enumerable<string> | Date | string
    lt?: Date | string
    lte?: Date | string
    gt?: Date | string
    gte?: Date | string
    not?: NestedDateTimeWithAggregatesFilter | Date | string
    _count?: NestedIntFilter
    _min?: NestedDateTimeFilter
    _max?: NestedDateTimeFilter
  }

  export type EnumArtTypeFilter = {
    equals?: ArtType
    in?: Enumerable<ArtType>
    notIn?: Enumerable<ArtType>
    not?: NestedEnumArtTypeFilter | ArtType
  }

  export type StringNullableFilter = {
    equals?: string | null
    in?: Enumerable<string> | string | null
    notIn?: Enumerable<string> | string | null
    lt?: string
    lte?: string
    gt?: string
    gte?: string
    contains?: string
    startsWith?: string
    endsWith?: string
    mode?: QueryMode
    not?: NestedStringNullableFilter | string | null
  }

  export type GuildRelationFilter = {
    is?: GuildWhereInput
    isNot?: GuildWhereInput
  }

  export type AttackListRelationFilter = {
    every?: AttackWhereInput
    some?: AttackWhereInput
    none?: AttackWhereInput
  }

  export type AttackOrderByRelationAggregateInput = {
    _count?: SortOrder
  }

  export type ArtKeyGuild_idCompoundUniqueInput = {
    key: string
    guild_id: string
  }

  export type ArtCountOrderByAggregateInput = {
    name?: SortOrder
    key?: SortOrder
    type?: SortOrder
    role?: SortOrder
    guild_id?: SortOrder
    embed_title?: SortOrder
    embed_description?: SortOrder
    embed_url?: SortOrder
    created_at?: SortOrder
    updated_at?: SortOrder
  }

  export type ArtMaxOrderByAggregateInput = {
    name?: SortOrder
    key?: SortOrder
    type?: SortOrder
    role?: SortOrder
    guild_id?: SortOrder
    embed_title?: SortOrder
    embed_description?: SortOrder
    embed_url?: SortOrder
    created_at?: SortOrder
    updated_at?: SortOrder
  }

  export type ArtMinOrderByAggregateInput = {
    name?: SortOrder
    key?: SortOrder
    type?: SortOrder
    role?: SortOrder
    guild_id?: SortOrder
    embed_title?: SortOrder
    embed_description?: SortOrder
    embed_url?: SortOrder
    created_at?: SortOrder
    updated_at?: SortOrder
  }

  export type EnumArtTypeWithAggregatesFilter = {
    equals?: ArtType
    in?: Enumerable<ArtType>
    notIn?: Enumerable<ArtType>
    not?: NestedEnumArtTypeWithAggregatesFilter | ArtType
    _count?: NestedIntFilter
    _min?: NestedEnumArtTypeFilter
    _max?: NestedEnumArtTypeFilter
  }

  export type StringNullableWithAggregatesFilter = {
    equals?: string | null
    in?: Enumerable<string> | string | null
    notIn?: Enumerable<string> | string | null
    lt?: string
    lte?: string
    gt?: string
    gte?: string
    contains?: string
    startsWith?: string
    endsWith?: string
    mode?: QueryMode
    not?: NestedStringNullableWithAggregatesFilter | string | null
    _count?: NestedIntNullableFilter
    _min?: NestedStringNullableFilter
    _max?: NestedStringNullableFilter
  }

  export type StringNullableListFilter = {
    equals?: Enumerable<string> | null
    has?: string | null
    hasEvery?: Enumerable<string>
    hasSome?: Enumerable<string>
    isEmpty?: boolean
  }

  export type IntFilter = {
    equals?: number
    in?: Enumerable<number> | number
    notIn?: Enumerable<number> | number
    lt?: number
    lte?: number
    gt?: number
    gte?: number
    not?: NestedIntFilter | number
  }

  export type ArtRelationFilter = {
    is?: ArtWhereInput
    isNot?: ArtWhereInput
  }

  export type AttackKeyGuild_idCompoundUniqueInput = {
    key: string
    guild_id: string
  }

  export type AttackCountOrderByAggregateInput = {
    name?: SortOrder
    key?: SortOrder
    art_key?: SortOrder
    guild_id?: SortOrder
    roles?: SortOrder
    required_roles?: SortOrder
    required_exp?: SortOrder
    damage?: SortOrder
    stamina?: SortOrder
    embed_title?: SortOrder
    embed_description?: SortOrder
    embed_url?: SortOrder
    fields_key?: SortOrder
    created_at?: SortOrder
    updated_at?: SortOrder
  }

  export type AttackAvgOrderByAggregateInput = {
    required_roles?: SortOrder
    required_exp?: SortOrder
    damage?: SortOrder
    stamina?: SortOrder
  }

  export type AttackMaxOrderByAggregateInput = {
    name?: SortOrder
    key?: SortOrder
    art_key?: SortOrder
    guild_id?: SortOrder
    required_roles?: SortOrder
    required_exp?: SortOrder
    damage?: SortOrder
    stamina?: SortOrder
    embed_title?: SortOrder
    embed_description?: SortOrder
    embed_url?: SortOrder
    fields_key?: SortOrder
    created_at?: SortOrder
    updated_at?: SortOrder
  }

  export type AttackMinOrderByAggregateInput = {
    name?: SortOrder
    key?: SortOrder
    art_key?: SortOrder
    guild_id?: SortOrder
    required_roles?: SortOrder
    required_exp?: SortOrder
    damage?: SortOrder
    stamina?: SortOrder
    embed_title?: SortOrder
    embed_description?: SortOrder
    embed_url?: SortOrder
    fields_key?: SortOrder
    created_at?: SortOrder
    updated_at?: SortOrder
  }

  export type AttackSumOrderByAggregateInput = {
    required_roles?: SortOrder
    required_exp?: SortOrder
    damage?: SortOrder
    stamina?: SortOrder
  }

  export type IntWithAggregatesFilter = {
    equals?: number
    in?: Enumerable<number> | number
    notIn?: Enumerable<number> | number
    lt?: number
    lte?: number
    gt?: number
    gte?: number
    not?: NestedIntWithAggregatesFilter | number
    _count?: NestedIntFilter
    _avg?: NestedFloatFilter
    _sum?: NestedIntFilter
    _min?: NestedIntFilter
    _max?: NestedIntFilter
  }

  export type BoolFilter = {
    equals?: boolean
    not?: NestedBoolFilter | boolean
  }

  export type VarialbleGuild_idNameCompoundUniqueInput = {
    guild_id: string
    name: string
  }

  export type VarialbleCountOrderByAggregateInput = {
    guild_id?: SortOrder
    name?: SortOrder
    text?: SortOrder
    visibleCaseIfNotAuthorizerMember?: SortOrder
    required_roles?: SortOrder
    roles?: SortOrder
    created_at?: SortOrder
    updated_at?: SortOrder
  }

  export type VarialbleAvgOrderByAggregateInput = {
    required_roles?: SortOrder
  }

  export type VarialbleMaxOrderByAggregateInput = {
    guild_id?: SortOrder
    name?: SortOrder
    text?: SortOrder
    visibleCaseIfNotAuthorizerMember?: SortOrder
    required_roles?: SortOrder
    created_at?: SortOrder
    updated_at?: SortOrder
  }

  export type VarialbleMinOrderByAggregateInput = {
    guild_id?: SortOrder
    name?: SortOrder
    text?: SortOrder
    visibleCaseIfNotAuthorizerMember?: SortOrder
    required_roles?: SortOrder
    created_at?: SortOrder
    updated_at?: SortOrder
  }

  export type VarialbleSumOrderByAggregateInput = {
    required_roles?: SortOrder
  }

  export type BoolWithAggregatesFilter = {
    equals?: boolean
    not?: NestedBoolWithAggregatesFilter | boolean
    _count?: NestedIntFilter
    _min?: NestedBoolFilter
    _max?: NestedBoolFilter
  }

  export type ArtCreateNestedManyWithoutGuildInput = {
    create?: XOR<Enumerable<ArtCreateWithoutGuildInput>, Enumerable<ArtUncheckedCreateWithoutGuildInput>>
    connectOrCreate?: Enumerable<ArtCreateOrConnectWithoutGuildInput>
    createMany?: ArtCreateManyGuildInputEnvelope
    connect?: Enumerable<ArtWhereUniqueInput>
  }

  export type VarialbleCreateNestedManyWithoutGuildInput = {
    create?: XOR<Enumerable<VarialbleCreateWithoutGuildInput>, Enumerable<VarialbleUncheckedCreateWithoutGuildInput>>
    connectOrCreate?: Enumerable<VarialbleCreateOrConnectWithoutGuildInput>
    createMany?: VarialbleCreateManyGuildInputEnvelope
    connect?: Enumerable<VarialbleWhereUniqueInput>
  }

  export type ArtUncheckedCreateNestedManyWithoutGuildInput = {
    create?: XOR<Enumerable<ArtCreateWithoutGuildInput>, Enumerable<ArtUncheckedCreateWithoutGuildInput>>
    connectOrCreate?: Enumerable<ArtCreateOrConnectWithoutGuildInput>
    createMany?: ArtCreateManyGuildInputEnvelope
    connect?: Enumerable<ArtWhereUniqueInput>
  }

  export type VarialbleUncheckedCreateNestedManyWithoutGuildInput = {
    create?: XOR<Enumerable<VarialbleCreateWithoutGuildInput>, Enumerable<VarialbleUncheckedCreateWithoutGuildInput>>
    connectOrCreate?: Enumerable<VarialbleCreateOrConnectWithoutGuildInput>
    createMany?: VarialbleCreateManyGuildInputEnvelope
    connect?: Enumerable<VarialbleWhereUniqueInput>
  }

  export type StringFieldUpdateOperationsInput = {
    set?: string
  }

  export type DateTimeFieldUpdateOperationsInput = {
    set?: Date | string
  }

  export type ArtUpdateManyWithoutGuildNestedInput = {
    create?: XOR<Enumerable<ArtCreateWithoutGuildInput>, Enumerable<ArtUncheckedCreateWithoutGuildInput>>
    connectOrCreate?: Enumerable<ArtCreateOrConnectWithoutGuildInput>
    upsert?: Enumerable<ArtUpsertWithWhereUniqueWithoutGuildInput>
    createMany?: ArtCreateManyGuildInputEnvelope
    set?: Enumerable<ArtWhereUniqueInput>
    disconnect?: Enumerable<ArtWhereUniqueInput>
    delete?: Enumerable<ArtWhereUniqueInput>
    connect?: Enumerable<ArtWhereUniqueInput>
    update?: Enumerable<ArtUpdateWithWhereUniqueWithoutGuildInput>
    updateMany?: Enumerable<ArtUpdateManyWithWhereWithoutGuildInput>
    deleteMany?: Enumerable<ArtScalarWhereInput>
  }

  export type VarialbleUpdateManyWithoutGuildNestedInput = {
    create?: XOR<Enumerable<VarialbleCreateWithoutGuildInput>, Enumerable<VarialbleUncheckedCreateWithoutGuildInput>>
    connectOrCreate?: Enumerable<VarialbleCreateOrConnectWithoutGuildInput>
    upsert?: Enumerable<VarialbleUpsertWithWhereUniqueWithoutGuildInput>
    createMany?: VarialbleCreateManyGuildInputEnvelope
    set?: Enumerable<VarialbleWhereUniqueInput>
    disconnect?: Enumerable<VarialbleWhereUniqueInput>
    delete?: Enumerable<VarialbleWhereUniqueInput>
    connect?: Enumerable<VarialbleWhereUniqueInput>
    update?: Enumerable<VarialbleUpdateWithWhereUniqueWithoutGuildInput>
    updateMany?: Enumerable<VarialbleUpdateManyWithWhereWithoutGuildInput>
    deleteMany?: Enumerable<VarialbleScalarWhereInput>
  }

  export type ArtUncheckedUpdateManyWithoutGuildNestedInput = {
    create?: XOR<Enumerable<ArtCreateWithoutGuildInput>, Enumerable<ArtUncheckedCreateWithoutGuildInput>>
    connectOrCreate?: Enumerable<ArtCreateOrConnectWithoutGuildInput>
    upsert?: Enumerable<ArtUpsertWithWhereUniqueWithoutGuildInput>
    createMany?: ArtCreateManyGuildInputEnvelope
    set?: Enumerable<ArtWhereUniqueInput>
    disconnect?: Enumerable<ArtWhereUniqueInput>
    delete?: Enumerable<ArtWhereUniqueInput>
    connect?: Enumerable<ArtWhereUniqueInput>
    update?: Enumerable<ArtUpdateWithWhereUniqueWithoutGuildInput>
    updateMany?: Enumerable<ArtUpdateManyWithWhereWithoutGuildInput>
    deleteMany?: Enumerable<ArtScalarWhereInput>
  }

  export type VarialbleUncheckedUpdateManyWithoutGuildNestedInput = {
    create?: XOR<Enumerable<VarialbleCreateWithoutGuildInput>, Enumerable<VarialbleUncheckedCreateWithoutGuildInput>>
    connectOrCreate?: Enumerable<VarialbleCreateOrConnectWithoutGuildInput>
    upsert?: Enumerable<VarialbleUpsertWithWhereUniqueWithoutGuildInput>
    createMany?: VarialbleCreateManyGuildInputEnvelope
    set?: Enumerable<VarialbleWhereUniqueInput>
    disconnect?: Enumerable<VarialbleWhereUniqueInput>
    delete?: Enumerable<VarialbleWhereUniqueInput>
    connect?: Enumerable<VarialbleWhereUniqueInput>
    update?: Enumerable<VarialbleUpdateWithWhereUniqueWithoutGuildInput>
    updateMany?: Enumerable<VarialbleUpdateManyWithWhereWithoutGuildInput>
    deleteMany?: Enumerable<VarialbleScalarWhereInput>
  }

  export type GuildCreateNestedOneWithoutArtsInput = {
    create?: XOR<GuildCreateWithoutArtsInput, GuildUncheckedCreateWithoutArtsInput>
    connectOrCreate?: GuildCreateOrConnectWithoutArtsInput
    connect?: GuildWhereUniqueInput
  }

  export type AttackCreateNestedManyWithoutArtInput = {
    create?: XOR<Enumerable<AttackCreateWithoutArtInput>, Enumerable<AttackUncheckedCreateWithoutArtInput>>
    connectOrCreate?: Enumerable<AttackCreateOrConnectWithoutArtInput>
    createMany?: AttackCreateManyArtInputEnvelope
    connect?: Enumerable<AttackWhereUniqueInput>
  }

  export type AttackUncheckedCreateNestedManyWithoutArtInput = {
    create?: XOR<Enumerable<AttackCreateWithoutArtInput>, Enumerable<AttackUncheckedCreateWithoutArtInput>>
    connectOrCreate?: Enumerable<AttackCreateOrConnectWithoutArtInput>
    createMany?: AttackCreateManyArtInputEnvelope
    connect?: Enumerable<AttackWhereUniqueInput>
  }

  export type EnumArtTypeFieldUpdateOperationsInput = {
    set?: ArtType
  }

  export type NullableStringFieldUpdateOperationsInput = {
    set?: string | null
  }

  export type GuildUpdateOneRequiredWithoutArtsNestedInput = {
    create?: XOR<GuildCreateWithoutArtsInput, GuildUncheckedCreateWithoutArtsInput>
    connectOrCreate?: GuildCreateOrConnectWithoutArtsInput
    upsert?: GuildUpsertWithoutArtsInput
    connect?: GuildWhereUniqueInput
    update?: XOR<GuildUpdateWithoutArtsInput, GuildUncheckedUpdateWithoutArtsInput>
  }

  export type AttackUpdateManyWithoutArtNestedInput = {
    create?: XOR<Enumerable<AttackCreateWithoutArtInput>, Enumerable<AttackUncheckedCreateWithoutArtInput>>
    connectOrCreate?: Enumerable<AttackCreateOrConnectWithoutArtInput>
    upsert?: Enumerable<AttackUpsertWithWhereUniqueWithoutArtInput>
    createMany?: AttackCreateManyArtInputEnvelope
    set?: Enumerable<AttackWhereUniqueInput>
    disconnect?: Enumerable<AttackWhereUniqueInput>
    delete?: Enumerable<AttackWhereUniqueInput>
    connect?: Enumerable<AttackWhereUniqueInput>
    update?: Enumerable<AttackUpdateWithWhereUniqueWithoutArtInput>
    updateMany?: Enumerable<AttackUpdateManyWithWhereWithoutArtInput>
    deleteMany?: Enumerable<AttackScalarWhereInput>
  }

  export type AttackUncheckedUpdateManyWithoutArtNestedInput = {
    create?: XOR<Enumerable<AttackCreateWithoutArtInput>, Enumerable<AttackUncheckedCreateWithoutArtInput>>
    connectOrCreate?: Enumerable<AttackCreateOrConnectWithoutArtInput>
    upsert?: Enumerable<AttackUpsertWithWhereUniqueWithoutArtInput>
    createMany?: AttackCreateManyArtInputEnvelope
    set?: Enumerable<AttackWhereUniqueInput>
    disconnect?: Enumerable<AttackWhereUniqueInput>
    delete?: Enumerable<AttackWhereUniqueInput>
    connect?: Enumerable<AttackWhereUniqueInput>
    update?: Enumerable<AttackUpdateWithWhereUniqueWithoutArtInput>
    updateMany?: Enumerable<AttackUpdateManyWithWhereWithoutArtInput>
    deleteMany?: Enumerable<AttackScalarWhereInput>
  }

  export type AttackCreaterolesInput = {
    set: Enumerable<string>
  }

  export type ArtCreateNestedOneWithoutAttacksInput = {
    create?: XOR<ArtCreateWithoutAttacksInput, ArtUncheckedCreateWithoutAttacksInput>
    connectOrCreate?: ArtCreateOrConnectWithoutAttacksInput
    connect?: ArtWhereUniqueInput
  }

  export type AttackUpdaterolesInput = {
    set?: Enumerable<string>
    push?: string | Enumerable<string>
  }

  export type IntFieldUpdateOperationsInput = {
    set?: number
    increment?: number
    decrement?: number
    multiply?: number
    divide?: number
  }

  export type ArtUpdateOneRequiredWithoutAttacksNestedInput = {
    create?: XOR<ArtCreateWithoutAttacksInput, ArtUncheckedCreateWithoutAttacksInput>
    connectOrCreate?: ArtCreateOrConnectWithoutAttacksInput
    upsert?: ArtUpsertWithoutAttacksInput
    connect?: ArtWhereUniqueInput
    update?: XOR<ArtUpdateWithoutAttacksInput, ArtUncheckedUpdateWithoutAttacksInput>
  }

  export type VarialbleCreaterolesInput = {
    set: Enumerable<string>
  }

  export type GuildCreateNestedOneWithoutVarsInput = {
    create?: XOR<GuildCreateWithoutVarsInput, GuildUncheckedCreateWithoutVarsInput>
    connectOrCreate?: GuildCreateOrConnectWithoutVarsInput
    connect?: GuildWhereUniqueInput
  }

  export type BoolFieldUpdateOperationsInput = {
    set?: boolean
  }

  export type VarialbleUpdaterolesInput = {
    set?: Enumerable<string>
    push?: string | Enumerable<string>
  }

  export type GuildUpdateOneRequiredWithoutVarsNestedInput = {
    create?: XOR<GuildCreateWithoutVarsInput, GuildUncheckedCreateWithoutVarsInput>
    connectOrCreate?: GuildCreateOrConnectWithoutVarsInput
    upsert?: GuildUpsertWithoutVarsInput
    connect?: GuildWhereUniqueInput
    update?: XOR<GuildUpdateWithoutVarsInput, GuildUncheckedUpdateWithoutVarsInput>
  }

  export type NestedStringFilter = {
    equals?: string
    in?: Enumerable<string> | string
    notIn?: Enumerable<string> | string
    lt?: string
    lte?: string
    gt?: string
    gte?: string
    contains?: string
    startsWith?: string
    endsWith?: string
    not?: NestedStringFilter | string
  }

  export type NestedDateTimeFilter = {
    equals?: Date | string
    in?: Enumerable<Date> | Enumerable<string> | Date | string
    notIn?: Enumerable<Date> | Enumerable<string> | Date | string
    lt?: Date | string
    lte?: Date | string
    gt?: Date | string
    gte?: Date | string
    not?: NestedDateTimeFilter | Date | string
  }

  export type NestedStringWithAggregatesFilter = {
    equals?: string
    in?: Enumerable<string> | string
    notIn?: Enumerable<string> | string
    lt?: string
    lte?: string
    gt?: string
    gte?: string
    contains?: string
    startsWith?: string
    endsWith?: string
    not?: NestedStringWithAggregatesFilter | string
    _count?: NestedIntFilter
    _min?: NestedStringFilter
    _max?: NestedStringFilter
  }

  export type NestedIntFilter = {
    equals?: number
    in?: Enumerable<number> | number
    notIn?: Enumerable<number> | number
    lt?: number
    lte?: number
    gt?: number
    gte?: number
    not?: NestedIntFilter | number
  }

  export type NestedDateTimeWithAggregatesFilter = {
    equals?: Date | string
    in?: Enumerable<Date> | Enumerable<string> | Date | string
    notIn?: Enumerable<Date> | Enumerable<string> | Date | string
    lt?: Date | string
    lte?: Date | string
    gt?: Date | string
    gte?: Date | string
    not?: NestedDateTimeWithAggregatesFilter | Date | string
    _count?: NestedIntFilter
    _min?: NestedDateTimeFilter
    _max?: NestedDateTimeFilter
  }

  export type NestedEnumArtTypeFilter = {
    equals?: ArtType
    in?: Enumerable<ArtType>
    notIn?: Enumerable<ArtType>
    not?: NestedEnumArtTypeFilter | ArtType
  }

  export type NestedStringNullableFilter = {
    equals?: string | null
    in?: Enumerable<string> | string | null
    notIn?: Enumerable<string> | string | null
    lt?: string
    lte?: string
    gt?: string
    gte?: string
    contains?: string
    startsWith?: string
    endsWith?: string
    not?: NestedStringNullableFilter | string | null
  }

  export type NestedEnumArtTypeWithAggregatesFilter = {
    equals?: ArtType
    in?: Enumerable<ArtType>
    notIn?: Enumerable<ArtType>
    not?: NestedEnumArtTypeWithAggregatesFilter | ArtType
    _count?: NestedIntFilter
    _min?: NestedEnumArtTypeFilter
    _max?: NestedEnumArtTypeFilter
  }

  export type NestedStringNullableWithAggregatesFilter = {
    equals?: string | null
    in?: Enumerable<string> | string | null
    notIn?: Enumerable<string> | string | null
    lt?: string
    lte?: string
    gt?: string
    gte?: string
    contains?: string
    startsWith?: string
    endsWith?: string
    not?: NestedStringNullableWithAggregatesFilter | string | null
    _count?: NestedIntNullableFilter
    _min?: NestedStringNullableFilter
    _max?: NestedStringNullableFilter
  }

  export type NestedIntNullableFilter = {
    equals?: number | null
    in?: Enumerable<number> | number | null
    notIn?: Enumerable<number> | number | null
    lt?: number
    lte?: number
    gt?: number
    gte?: number
    not?: NestedIntNullableFilter | number | null
  }

  export type NestedIntWithAggregatesFilter = {
    equals?: number
    in?: Enumerable<number> | number
    notIn?: Enumerable<number> | number
    lt?: number
    lte?: number
    gt?: number
    gte?: number
    not?: NestedIntWithAggregatesFilter | number
    _count?: NestedIntFilter
    _avg?: NestedFloatFilter
    _sum?: NestedIntFilter
    _min?: NestedIntFilter
    _max?: NestedIntFilter
  }

  export type NestedFloatFilter = {
    equals?: number
    in?: Enumerable<number> | number
    notIn?: Enumerable<number> | number
    lt?: number
    lte?: number
    gt?: number
    gte?: number
    not?: NestedFloatFilter | number
  }

  export type NestedBoolFilter = {
    equals?: boolean
    not?: NestedBoolFilter | boolean
  }

  export type NestedBoolWithAggregatesFilter = {
    equals?: boolean
    not?: NestedBoolWithAggregatesFilter | boolean
    _count?: NestedIntFilter
    _min?: NestedBoolFilter
    _max?: NestedBoolFilter
  }

  export type ArtCreateWithoutGuildInput = {
    name: string
    key: string
    type: ArtType
    role?: string | null
    embed_title?: string | null
    embed_description?: string | null
    embed_url?: string | null
    created_at?: Date | string
    updated_at?: Date | string
    attacks?: AttackCreateNestedManyWithoutArtInput
  }

  export type ArtUncheckedCreateWithoutGuildInput = {
    name: string
    key: string
    type: ArtType
    role?: string | null
    embed_title?: string | null
    embed_description?: string | null
    embed_url?: string | null
    created_at?: Date | string
    updated_at?: Date | string
    attacks?: AttackUncheckedCreateNestedManyWithoutArtInput
  }

  export type ArtCreateOrConnectWithoutGuildInput = {
    where: ArtWhereUniqueInput
    create: XOR<ArtCreateWithoutGuildInput, ArtUncheckedCreateWithoutGuildInput>
  }

  export type ArtCreateManyGuildInputEnvelope = {
    data: Enumerable<ArtCreateManyGuildInput>
    skipDuplicates?: boolean
  }

  export type VarialbleCreateWithoutGuildInput = {
    name: string
    text: string
    visibleCaseIfNotAuthorizerMember?: boolean
    required_roles?: number
    roles?: VarialbleCreaterolesInput | Enumerable<string>
    created_at?: Date | string
    updated_at?: Date | string
  }

  export type VarialbleUncheckedCreateWithoutGuildInput = {
    name: string
    text: string
    visibleCaseIfNotAuthorizerMember?: boolean
    required_roles?: number
    roles?: VarialbleCreaterolesInput | Enumerable<string>
    created_at?: Date | string
    updated_at?: Date | string
  }

  export type VarialbleCreateOrConnectWithoutGuildInput = {
    where: VarialbleWhereUniqueInput
    create: XOR<VarialbleCreateWithoutGuildInput, VarialbleUncheckedCreateWithoutGuildInput>
  }

  export type VarialbleCreateManyGuildInputEnvelope = {
    data: Enumerable<VarialbleCreateManyGuildInput>
    skipDuplicates?: boolean
  }

  export type ArtUpsertWithWhereUniqueWithoutGuildInput = {
    where: ArtWhereUniqueInput
    update: XOR<ArtUpdateWithoutGuildInput, ArtUncheckedUpdateWithoutGuildInput>
    create: XOR<ArtCreateWithoutGuildInput, ArtUncheckedCreateWithoutGuildInput>
  }

  export type ArtUpdateWithWhereUniqueWithoutGuildInput = {
    where: ArtWhereUniqueInput
    data: XOR<ArtUpdateWithoutGuildInput, ArtUncheckedUpdateWithoutGuildInput>
  }

  export type ArtUpdateManyWithWhereWithoutGuildInput = {
    where: ArtScalarWhereInput
    data: XOR<ArtUpdateManyMutationInput, ArtUncheckedUpdateManyWithoutArtsInput>
  }

  export type ArtScalarWhereInput = {
    AND?: Enumerable<ArtScalarWhereInput>
    OR?: Enumerable<ArtScalarWhereInput>
    NOT?: Enumerable<ArtScalarWhereInput>
    name?: StringFilter | string
    key?: StringFilter | string
    type?: EnumArtTypeFilter | ArtType
    role?: StringNullableFilter | string | null
    guild_id?: StringFilter | string
    embed_title?: StringNullableFilter | string | null
    embed_description?: StringNullableFilter | string | null
    embed_url?: StringNullableFilter | string | null
    created_at?: DateTimeFilter | Date | string
    updated_at?: DateTimeFilter | Date | string
  }

  export type VarialbleUpsertWithWhereUniqueWithoutGuildInput = {
    where: VarialbleWhereUniqueInput
    update: XOR<VarialbleUpdateWithoutGuildInput, VarialbleUncheckedUpdateWithoutGuildInput>
    create: XOR<VarialbleCreateWithoutGuildInput, VarialbleUncheckedCreateWithoutGuildInput>
  }

  export type VarialbleUpdateWithWhereUniqueWithoutGuildInput = {
    where: VarialbleWhereUniqueInput
    data: XOR<VarialbleUpdateWithoutGuildInput, VarialbleUncheckedUpdateWithoutGuildInput>
  }

  export type VarialbleUpdateManyWithWhereWithoutGuildInput = {
    where: VarialbleScalarWhereInput
    data: XOR<VarialbleUpdateManyMutationInput, VarialbleUncheckedUpdateManyWithoutVarsInput>
  }

  export type VarialbleScalarWhereInput = {
    AND?: Enumerable<VarialbleScalarWhereInput>
    OR?: Enumerable<VarialbleScalarWhereInput>
    NOT?: Enumerable<VarialbleScalarWhereInput>
    guild_id?: StringFilter | string
    name?: StringFilter | string
    text?: StringFilter | string
    visibleCaseIfNotAuthorizerMember?: BoolFilter | boolean
    required_roles?: IntFilter | number
    roles?: StringNullableListFilter
    created_at?: DateTimeFilter | Date | string
    updated_at?: DateTimeFilter | Date | string
  }

  export type GuildCreateWithoutArtsInput = {
    id: string
    created_at?: Date | string
    updated_at?: Date | string
    vars?: VarialbleCreateNestedManyWithoutGuildInput
  }

  export type GuildUncheckedCreateWithoutArtsInput = {
    id: string
    created_at?: Date | string
    updated_at?: Date | string
    vars?: VarialbleUncheckedCreateNestedManyWithoutGuildInput
  }

  export type GuildCreateOrConnectWithoutArtsInput = {
    where: GuildWhereUniqueInput
    create: XOR<GuildCreateWithoutArtsInput, GuildUncheckedCreateWithoutArtsInput>
  }

  export type AttackCreateWithoutArtInput = {
    name: string
    key: string
    roles?: AttackCreaterolesInput | Enumerable<string>
    required_roles?: number
    required_exp?: number
    damage?: number
    stamina?: number
    embed_title?: string | null
    embed_description?: string | null
    embed_url?: string | null
    fields_key?: string | null
    created_at?: Date | string
    updated_at?: Date | string
  }

  export type AttackUncheckedCreateWithoutArtInput = {
    name: string
    key: string
    roles?: AttackCreaterolesInput | Enumerable<string>
    required_roles?: number
    required_exp?: number
    damage?: number
    stamina?: number
    embed_title?: string | null
    embed_description?: string | null
    embed_url?: string | null
    fields_key?: string | null
    created_at?: Date | string
    updated_at?: Date | string
  }

  export type AttackCreateOrConnectWithoutArtInput = {
    where: AttackWhereUniqueInput
    create: XOR<AttackCreateWithoutArtInput, AttackUncheckedCreateWithoutArtInput>
  }

  export type AttackCreateManyArtInputEnvelope = {
    data: Enumerable<AttackCreateManyArtInput>
    skipDuplicates?: boolean
  }

  export type GuildUpsertWithoutArtsInput = {
    update: XOR<GuildUpdateWithoutArtsInput, GuildUncheckedUpdateWithoutArtsInput>
    create: XOR<GuildCreateWithoutArtsInput, GuildUncheckedCreateWithoutArtsInput>
  }

  export type GuildUpdateWithoutArtsInput = {
    id?: StringFieldUpdateOperationsInput | string
    created_at?: DateTimeFieldUpdateOperationsInput | Date | string
    updated_at?: DateTimeFieldUpdateOperationsInput | Date | string
    vars?: VarialbleUpdateManyWithoutGuildNestedInput
  }

  export type GuildUncheckedUpdateWithoutArtsInput = {
    id?: StringFieldUpdateOperationsInput | string
    created_at?: DateTimeFieldUpdateOperationsInput | Date | string
    updated_at?: DateTimeFieldUpdateOperationsInput | Date | string
    vars?: VarialbleUncheckedUpdateManyWithoutGuildNestedInput
  }

  export type AttackUpsertWithWhereUniqueWithoutArtInput = {
    where: AttackWhereUniqueInput
    update: XOR<AttackUpdateWithoutArtInput, AttackUncheckedUpdateWithoutArtInput>
    create: XOR<AttackCreateWithoutArtInput, AttackUncheckedCreateWithoutArtInput>
  }

  export type AttackUpdateWithWhereUniqueWithoutArtInput = {
    where: AttackWhereUniqueInput
    data: XOR<AttackUpdateWithoutArtInput, AttackUncheckedUpdateWithoutArtInput>
  }

  export type AttackUpdateManyWithWhereWithoutArtInput = {
    where: AttackScalarWhereInput
    data: XOR<AttackUpdateManyMutationInput, AttackUncheckedUpdateManyWithoutAttacksInput>
  }

  export type AttackScalarWhereInput = {
    AND?: Enumerable<AttackScalarWhereInput>
    OR?: Enumerable<AttackScalarWhereInput>
    NOT?: Enumerable<AttackScalarWhereInput>
    name?: StringFilter | string
    key?: StringFilter | string
    art_key?: StringFilter | string
    guild_id?: StringFilter | string
    roles?: StringNullableListFilter
    required_roles?: IntFilter | number
    required_exp?: IntFilter | number
    damage?: IntFilter | number
    stamina?: IntFilter | number
    embed_title?: StringNullableFilter | string | null
    embed_description?: StringNullableFilter | string | null
    embed_url?: StringNullableFilter | string | null
    fields_key?: StringNullableFilter | string | null
    created_at?: DateTimeFilter | Date | string
    updated_at?: DateTimeFilter | Date | string
  }

  export type ArtCreateWithoutAttacksInput = {
    name: string
    key: string
    type: ArtType
    role?: string | null
    embed_title?: string | null
    embed_description?: string | null
    embed_url?: string | null
    created_at?: Date | string
    updated_at?: Date | string
    guild: GuildCreateNestedOneWithoutArtsInput
  }

  export type ArtUncheckedCreateWithoutAttacksInput = {
    name: string
    key: string
    type: ArtType
    role?: string | null
    guild_id: string
    embed_title?: string | null
    embed_description?: string | null
    embed_url?: string | null
    created_at?: Date | string
    updated_at?: Date | string
  }

  export type ArtCreateOrConnectWithoutAttacksInput = {
    where: ArtWhereUniqueInput
    create: XOR<ArtCreateWithoutAttacksInput, ArtUncheckedCreateWithoutAttacksInput>
  }

  export type ArtUpsertWithoutAttacksInput = {
    update: XOR<ArtUpdateWithoutAttacksInput, ArtUncheckedUpdateWithoutAttacksInput>
    create: XOR<ArtCreateWithoutAttacksInput, ArtUncheckedCreateWithoutAttacksInput>
  }

  export type ArtUpdateWithoutAttacksInput = {
    name?: StringFieldUpdateOperationsInput | string
    key?: StringFieldUpdateOperationsInput | string
    type?: EnumArtTypeFieldUpdateOperationsInput | ArtType
    role?: NullableStringFieldUpdateOperationsInput | string | null
    embed_title?: NullableStringFieldUpdateOperationsInput | string | null
    embed_description?: NullableStringFieldUpdateOperationsInput | string | null
    embed_url?: NullableStringFieldUpdateOperationsInput | string | null
    created_at?: DateTimeFieldUpdateOperationsInput | Date | string
    updated_at?: DateTimeFieldUpdateOperationsInput | Date | string
    guild?: GuildUpdateOneRequiredWithoutArtsNestedInput
  }

  export type ArtUncheckedUpdateWithoutAttacksInput = {
    name?: StringFieldUpdateOperationsInput | string
    key?: StringFieldUpdateOperationsInput | string
    type?: EnumArtTypeFieldUpdateOperationsInput | ArtType
    role?: NullableStringFieldUpdateOperationsInput | string | null
    guild_id?: StringFieldUpdateOperationsInput | string
    embed_title?: NullableStringFieldUpdateOperationsInput | string | null
    embed_description?: NullableStringFieldUpdateOperationsInput | string | null
    embed_url?: NullableStringFieldUpdateOperationsInput | string | null
    created_at?: DateTimeFieldUpdateOperationsInput | Date | string
    updated_at?: DateTimeFieldUpdateOperationsInput | Date | string
  }

  export type GuildCreateWithoutVarsInput = {
    id: string
    created_at?: Date | string
    updated_at?: Date | string
    arts?: ArtCreateNestedManyWithoutGuildInput
  }

  export type GuildUncheckedCreateWithoutVarsInput = {
    id: string
    created_at?: Date | string
    updated_at?: Date | string
    arts?: ArtUncheckedCreateNestedManyWithoutGuildInput
  }

  export type GuildCreateOrConnectWithoutVarsInput = {
    where: GuildWhereUniqueInput
    create: XOR<GuildCreateWithoutVarsInput, GuildUncheckedCreateWithoutVarsInput>
  }

  export type GuildUpsertWithoutVarsInput = {
    update: XOR<GuildUpdateWithoutVarsInput, GuildUncheckedUpdateWithoutVarsInput>
    create: XOR<GuildCreateWithoutVarsInput, GuildUncheckedCreateWithoutVarsInput>
  }

  export type GuildUpdateWithoutVarsInput = {
    id?: StringFieldUpdateOperationsInput | string
    created_at?: DateTimeFieldUpdateOperationsInput | Date | string
    updated_at?: DateTimeFieldUpdateOperationsInput | Date | string
    arts?: ArtUpdateManyWithoutGuildNestedInput
  }

  export type GuildUncheckedUpdateWithoutVarsInput = {
    id?: StringFieldUpdateOperationsInput | string
    created_at?: DateTimeFieldUpdateOperationsInput | Date | string
    updated_at?: DateTimeFieldUpdateOperationsInput | Date | string
    arts?: ArtUncheckedUpdateManyWithoutGuildNestedInput
  }

  export type ArtCreateManyGuildInput = {
    name: string
    key: string
    type: ArtType
    role?: string | null
    embed_title?: string | null
    embed_description?: string | null
    embed_url?: string | null
    created_at?: Date | string
    updated_at?: Date | string
  }

  export type VarialbleCreateManyGuildInput = {
    name: string
    text: string
    visibleCaseIfNotAuthorizerMember?: boolean
    required_roles?: number
    roles?: VarialbleCreaterolesInput | Enumerable<string>
    created_at?: Date | string
    updated_at?: Date | string
  }

  export type ArtUpdateWithoutGuildInput = {
    name?: StringFieldUpdateOperationsInput | string
    key?: StringFieldUpdateOperationsInput | string
    type?: EnumArtTypeFieldUpdateOperationsInput | ArtType
    role?: NullableStringFieldUpdateOperationsInput | string | null
    embed_title?: NullableStringFieldUpdateOperationsInput | string | null
    embed_description?: NullableStringFieldUpdateOperationsInput | string | null
    embed_url?: NullableStringFieldUpdateOperationsInput | string | null
    created_at?: DateTimeFieldUpdateOperationsInput | Date | string
    updated_at?: DateTimeFieldUpdateOperationsInput | Date | string
    attacks?: AttackUpdateManyWithoutArtNestedInput
  }

  export type ArtUncheckedUpdateWithoutGuildInput = {
    name?: StringFieldUpdateOperationsInput | string
    key?: StringFieldUpdateOperationsInput | string
    type?: EnumArtTypeFieldUpdateOperationsInput | ArtType
    role?: NullableStringFieldUpdateOperationsInput | string | null
    embed_title?: NullableStringFieldUpdateOperationsInput | string | null
    embed_description?: NullableStringFieldUpdateOperationsInput | string | null
    embed_url?: NullableStringFieldUpdateOperationsInput | string | null
    created_at?: DateTimeFieldUpdateOperationsInput | Date | string
    updated_at?: DateTimeFieldUpdateOperationsInput | Date | string
    attacks?: AttackUncheckedUpdateManyWithoutArtNestedInput
  }

  export type ArtUncheckedUpdateManyWithoutArtsInput = {
    name?: StringFieldUpdateOperationsInput | string
    key?: StringFieldUpdateOperationsInput | string
    type?: EnumArtTypeFieldUpdateOperationsInput | ArtType
    role?: NullableStringFieldUpdateOperationsInput | string | null
    embed_title?: NullableStringFieldUpdateOperationsInput | string | null
    embed_description?: NullableStringFieldUpdateOperationsInput | string | null
    embed_url?: NullableStringFieldUpdateOperationsInput | string | null
    created_at?: DateTimeFieldUpdateOperationsInput | Date | string
    updated_at?: DateTimeFieldUpdateOperationsInput | Date | string
  }

  export type VarialbleUpdateWithoutGuildInput = {
    name?: StringFieldUpdateOperationsInput | string
    text?: StringFieldUpdateOperationsInput | string
    visibleCaseIfNotAuthorizerMember?: BoolFieldUpdateOperationsInput | boolean
    required_roles?: IntFieldUpdateOperationsInput | number
    roles?: VarialbleUpdaterolesInput | Enumerable<string>
    created_at?: DateTimeFieldUpdateOperationsInput | Date | string
    updated_at?: DateTimeFieldUpdateOperationsInput | Date | string
  }

  export type VarialbleUncheckedUpdateWithoutGuildInput = {
    name?: StringFieldUpdateOperationsInput | string
    text?: StringFieldUpdateOperationsInput | string
    visibleCaseIfNotAuthorizerMember?: BoolFieldUpdateOperationsInput | boolean
    required_roles?: IntFieldUpdateOperationsInput | number
    roles?: VarialbleUpdaterolesInput | Enumerable<string>
    created_at?: DateTimeFieldUpdateOperationsInput | Date | string
    updated_at?: DateTimeFieldUpdateOperationsInput | Date | string
  }

  export type VarialbleUncheckedUpdateManyWithoutVarsInput = {
    name?: StringFieldUpdateOperationsInput | string
    text?: StringFieldUpdateOperationsInput | string
    visibleCaseIfNotAuthorizerMember?: BoolFieldUpdateOperationsInput | boolean
    required_roles?: IntFieldUpdateOperationsInput | number
    roles?: VarialbleUpdaterolesInput | Enumerable<string>
    created_at?: DateTimeFieldUpdateOperationsInput | Date | string
    updated_at?: DateTimeFieldUpdateOperationsInput | Date | string
  }

  export type AttackCreateManyArtInput = {
    name: string
    key: string
    roles?: AttackCreaterolesInput | Enumerable<string>
    required_roles?: number
    required_exp?: number
    damage?: number
    stamina?: number
    embed_title?: string | null
    embed_description?: string | null
    embed_url?: string | null
    fields_key?: string | null
    created_at?: Date | string
    updated_at?: Date | string
  }

  export type AttackUpdateWithoutArtInput = {
    name?: StringFieldUpdateOperationsInput | string
    key?: StringFieldUpdateOperationsInput | string
    roles?: AttackUpdaterolesInput | Enumerable<string>
    required_roles?: IntFieldUpdateOperationsInput | number
    required_exp?: IntFieldUpdateOperationsInput | number
    damage?: IntFieldUpdateOperationsInput | number
    stamina?: IntFieldUpdateOperationsInput | number
    embed_title?: NullableStringFieldUpdateOperationsInput | string | null
    embed_description?: NullableStringFieldUpdateOperationsInput | string | null
    embed_url?: NullableStringFieldUpdateOperationsInput | string | null
    fields_key?: NullableStringFieldUpdateOperationsInput | string | null
    created_at?: DateTimeFieldUpdateOperationsInput | Date | string
    updated_at?: DateTimeFieldUpdateOperationsInput | Date | string
  }

  export type AttackUncheckedUpdateWithoutArtInput = {
    name?: StringFieldUpdateOperationsInput | string
    key?: StringFieldUpdateOperationsInput | string
    roles?: AttackUpdaterolesInput | Enumerable<string>
    required_roles?: IntFieldUpdateOperationsInput | number
    required_exp?: IntFieldUpdateOperationsInput | number
    damage?: IntFieldUpdateOperationsInput | number
    stamina?: IntFieldUpdateOperationsInput | number
    embed_title?: NullableStringFieldUpdateOperationsInput | string | null
    embed_description?: NullableStringFieldUpdateOperationsInput | string | null
    embed_url?: NullableStringFieldUpdateOperationsInput | string | null
    fields_key?: NullableStringFieldUpdateOperationsInput | string | null
    created_at?: DateTimeFieldUpdateOperationsInput | Date | string
    updated_at?: DateTimeFieldUpdateOperationsInput | Date | string
  }

  export type AttackUncheckedUpdateManyWithoutAttacksInput = {
    name?: StringFieldUpdateOperationsInput | string
    key?: StringFieldUpdateOperationsInput | string
    roles?: AttackUpdaterolesInput | Enumerable<string>
    required_roles?: IntFieldUpdateOperationsInput | number
    required_exp?: IntFieldUpdateOperationsInput | number
    damage?: IntFieldUpdateOperationsInput | number
    stamina?: IntFieldUpdateOperationsInput | number
    embed_title?: NullableStringFieldUpdateOperationsInput | string | null
    embed_description?: NullableStringFieldUpdateOperationsInput | string | null
    embed_url?: NullableStringFieldUpdateOperationsInput | string | null
    fields_key?: NullableStringFieldUpdateOperationsInput | string | null
    created_at?: DateTimeFieldUpdateOperationsInput | Date | string
    updated_at?: DateTimeFieldUpdateOperationsInput | Date | string
  }



  /**
   * Batch Payload for updateMany & deleteMany & createMany
   */

  export type BatchPayload = {
    count: number
  }

  /**
   * DMMF
   */
  export const dmmf: runtime.BaseDMMF
}