import axios from "axios";
import { NextResponse } from "next/server";

const API = process.env.PRIVATE_API_DATA
export async function GET() {

    try {
        const res = await axios.get(`${API}/data/check_rating`)

        return NextResponse.json(res.data)
    } catch (error: unknown) {
        let message = 'Internal Server Error'
        let statusCode = 500
        if (axios.isAxiosError(error)) {
            message = error.response?.data?.message || message
            statusCode = error.response?.status || 500
        }
        return NextResponse.json({
            status: 0,
            message,
            data: {}
        }, { status: statusCode })
    }
}