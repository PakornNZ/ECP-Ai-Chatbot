"use client"

import "@/app/styles/style-Chat.css"
import { useEffect, useLayoutEffect, useRef, useState } from "react"
import { ManageChat, Arlert } from "@/app/components/object/object"
import { Pencil, Check, Copy } from 'lucide-react'
import axios from "axios"
import MarkdownRenderer from "@/app/components/MarkdownRenderer"
import { useSession } from "next-auth/react"
import Image from "next/image";
import chatBotIcon from "@/public/logo/logo.jpg"

interface Message {
    id: number | null
    query: string
    answer: string | null
    rating: number
}
    
interface SectionProps {
    MoveSection: boolean
    message: Message[]
    isLoading: boolean
    onUpdateQuery: (id: number, newQuery: string) => void
    onUpdateAnswer: (id: number, newAnswer: string) => void
}

export default function Chat({ MoveSection, message, isLoading, onUpdateQuery, onUpdateAnswer }: SectionProps) {

    const { data : session } = useSession()

        const chatbotSectionRef = useRef<HTMLDivElement>(null)

        useLayoutEffect(() => {
            if (chatbotSectionRef.current && message?.length) {
                chatbotSectionRef.current.scrollTop = chatbotSectionRef.current.scrollHeight
            }
        }, [message])


        // * ขนาด Textareaเริ่มต้น
        const textAreaEditRef = useRef<HTMLTextAreaElement>(null)

        const handleResize = () => {
            if (textAreaEditRef.current) {
                textAreaEditRef.current.style.height = "auto"
                textAreaEditRef.current.style.height = `${Math.min(textAreaEditRef.current.scrollHeight, 140)}px`
            }
        }
        
    const [isLoadingEdit, setIsLoadingEdit] = useState<boolean>(false)
    const [editIndex, setEditIndex] = useState<number | null>(null)
    const [editMessage, setEditMessage] = useState<string>("")
    const [isSubmit, setIsSubmit] = useState<boolean>(false)

    useEffect(() => {
        handleResize()
        setIsSubmit(false)
    }, [editIndex])
    
    const handleQueryEdit = (event: React.ChangeEvent<HTMLTextAreaElement>) => {
        const value = event.target.value
        setEditMessage(value)
        
        if (textAreaEditRef.current) {
            textAreaEditRef.current.style.height = "auto"
            textAreaEditRef.current.style.height = `${textAreaEditRef.current.scrollHeight}px`
        }

        setIsSubmit(value.trim().length > 0)
    }

            // * ข้อความแจ้งเตือน
            const [arlertMessage, setArlertMessage] = useState({
                color: true,
                message: ""
            })
                            const handleSaveEdit = async (msg_id: number) => {
                                if (msg_id === 0) return
                                const payload = {
                                    "msg_id": msg_id,
                                    "query": editMessage.trim()
                                }

                                setEditIndex(null)
                                setIsLoadingEdit(true)
                                onUpdateQuery(msg_id, editMessage.trim())

                                try {
                                    const res = await axios.put('/api/chat/edit_response', payload)
                                    const resData = res.data

                                    if (resData.status === 1) {
                                        onUpdateAnswer(msg_id, resData.data.answer)
                                    }
                                } catch (error: unknown) {
                                    if (!axios.isAxiosError(error)) return
                                    const errorMessage = error.response?.data?.message || "ระบบไม่สามารถตอบกลับได้ในขณะนี้"
                                    setArlertMessage({
                                        color: false,
                                        message: errorMessage
                                    })
                                    const timeOutAPI = setTimeout(() => {
                                        setArlertMessage({
                                            color: false,
                                            message: ""
                                        })
                                    }, 6000)
                                    return () => clearTimeout(timeOutAPI)
                                } finally {
                                    setIsLoadingEdit(false)
                                    setEditMessage("")
                                }
                            }


    // * คัดลอกข้อความ
    const [isCopy, setIsCopy] = useState<boolean>(false)
    const [playAnimation, setPlayAnimation] = useState<boolean>(false)

    const handleCopy = async (query: string) => {
        if (!query || isCopy) return

        try {
            if (window.isSecureContext && navigator.clipboard) {
                await navigator.clipboard.writeText(query)
            } else {
                // * ใช้แทน หากไม่มี https
                const textArea = document.createElement("textarea")
                textArea.value = query
                document.body.appendChild(textArea)
                textArea.focus()
                textArea.select()

                try {
                    document.execCommand('copy')
                } catch (error) {
                    console.error("Failed to copy: ", error)
                }
                document.body.removeChild(textArea)
            }

            // * เมื่อคัดลอกสำเร็จ
            setIsCopy(true)
            setPlayAnimation(true)
            setArlertMessage({
                color: true,
                message: "คัดลอกข้อความสำเร็จ"
            })

            const timeout = setTimeout(() => {
                setIsCopy(false)
                setPlayAnimation(true)
                setArlertMessage({
                    color: true,
                    message: ""
                })
            }, 6000)
            return () => clearTimeout(timeout)
        } catch (error) {
            console.error("Failed to copy: ", error)
        }
    }
    useEffect(() => {
        if (!playAnimation) return
        const timeout = setTimeout(() => setPlayAnimation(false), 500)
        return () => clearTimeout(timeout)
    }, [playAnimation])

    const [content, setContent] = useState<boolean>(false)
    // useEffect(() => {
    //     if (typeof session === "undefined") return
    //     fetchContent()
    // }, [session])

    const fetchContent = async () => {
        try {
            const res = await axios.get('/api/data/content/check')
            const resData = res.data
            if (resData.status === 1) {
                setContent(resData.data.status)
            }
        } catch (error) {
            if (!axios.isAxiosError(error)) return
            const errorMessage = error.response?.data?.message
            setArlertMessage({
                color: false,
                message: errorMessage
            })
            const timeOutAPI = setTimeout(() => {
                setArlertMessage({
                    color: false,
                    message: ""
                })
            }, 6000)
            return () => clearTimeout(timeOutAPI)
        }
    }

    return (
        <>
            <Arlert messageArlert={arlertMessage} />
            <div className="chatbot-section" ref={chatbotSectionRef}>
                <div className={`chatbot-center ${ MoveSection ? "" : "move"}`}>
                    {message?.map((e, index) => {
                        const isLast = index == (message.length - 1)
                        const isEdit = (editIndex == index) && session
                        const isWorkng = isLast && (isLoading || isLoadingEdit)

                        return (
                            <div key={index} className="chat-bubble">
                                <div className="chat-bubble-user">
                                    <div className={`chat-bubble-user-query ${ isEdit ? "edit" : ""}`}>
                                        { isEdit ? (
                                            <>
                                                <textarea 
                                                    ref={textAreaEditRef}
                                                    value={editMessage}
                                                    onChange={handleQueryEdit}
                                                    rows={1}
                                                    />
                                                <div className="edit-actions">
                                                    <button type="button" disabled={!isSubmit} left-title="แก้ไข" onClick={() => handleSaveEdit(e?.id || 0)}><Check /></button>
                                                    <button type="button" left-title="ยกเลิก" onClick={() => setEditIndex(null)}>ยกเลิก</button>
                                                </div>
                                            </>
                                        ) : (
                                            <span>{e?.query}</span>
                                        )}
                                    </div>

                                    { !isWorkng && isLast && !isEdit && session && (
                                        <div className="edit-chat-bubble">
                                            <button type="button" right-title="คัดลอก" onClick={() => handleCopy(e.query)} className={`copy-button ${playAnimation ? "play" : ""}`}>
                                                {isCopy ? <Check /> : <Copy />}
                                            </button>
                                            <button type="button" right-title="แก้ไขข้อความ" className="edit-button"
                                                onClick={() => {
                                                    setEditIndex(index)
                                                    setEditMessage(e?.query)
                                                }}
                                            >
                                                <Pencil/>
                                            </button>
                                        </div>
                                    )}
                                </div>
                                <div className="chat-bubble-bot">
                                    { isWorkng ? (
                                        <>
                                            <p className="skeleton skeleton-text" />
                                            <p className="skeleton skeleton-text" style={{ width: "70%" }} />
                                        </>
                                    ) : (
                                        <div style={{ display: "flex", gap: "10px" }}>
                                            <Image src={chatBotIcon} width={25} height={25} alt="chat-response" style={{ borderRadius: "50%" }}/>
                                            <span><MarkdownRenderer content={e?.answer || ""}/></span>
                                        </div>
                                    )}
                                </div>
                                { !isWorkng && <ManageChat msg_id={e?.id} answer={e?.answer} isRating={e?.rating} content={content}/>}
                            </div>
                        )
                    })}
                </div>
            </div>
        </>
    )
}

