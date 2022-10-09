import { EndpointBuilder } from '@reduxjs/toolkit/dist/query/endpointDefinitions'
import { BaseQueryFn, createApi, FetchArgs, fetchBaseQuery, FetchBaseQueryError, FetchBaseQueryMeta } from '@reduxjs/toolkit/query/react'

import { BASE_URL } from '../../utils/consts'

import { TUser } from './../../types/types'

export const authApi = createApi({
    baseQuery: fetchBaseQuery({
        baseUrl: BASE_URL,
    }),
    reducerPath: 'authApi',
    tagTypes: ['Auth'],
    endpoints: (build: EndpointBuilder<BaseQueryFn<
        string | FetchArgs,
        {},
        FetchBaseQueryError,
        {},
        FetchBaseQueryMeta>,
        'Auth',
        'authApi'>) => ({
            auth: build.query<TUser, { id: number }>({
                query(body: { id: number }) {
                    return {
                        url: '/api/auth',
                        method: 'POST',
                        body,
                    }
                },
                transformResponse: (response: { content: TUser }) => response?.content,
                // providesTags: [{ type: "Auth", id: "SCHEME" }],
            }),
        }),
})

export const {
    useAuthQuery,
} = authApi
