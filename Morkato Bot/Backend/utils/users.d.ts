interface UserTokenResponse {
  access_token: string
  token_type: string
  expires_in: number
  refresh_token: string
  scope: string
}

export declare function extractCode(code: string): Promise<UserTokenResponse | null>;
export declare function refreshToken(resfresh_token: string): Promise<UserTokenResponse | null>;
export declare function getUserResponse(token: string): Promise<Response>;