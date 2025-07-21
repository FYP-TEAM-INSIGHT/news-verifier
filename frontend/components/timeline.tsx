"use client"

import { cn } from "@/lib/utils"
import { CheckCircle, Clock, AlertCircle } from "lucide-react"

interface TimelineItem {
  step: string
  result: string
  status?: "completed" | "current" | "pending" | "error"
}

interface TimelineProps {
  items: TimelineItem[]
  className?: string
}

export function Timeline({ items, className }: TimelineProps) {
  return (
    <div className={cn("space-y-6", className)}>
      {items.map((item, index) => {
        const isLast = index === items.length - 1
        const status = item.status || "completed"

        const getIcon = () => {
          switch (status) {
            case "completed":
              return <CheckCircle className="h-5 w-5 text-green-500" />
            case "current":
              return <Clock className="h-5 w-5 text-blue-500" />
            case "error":
              return <AlertCircle className="h-5 w-5 text-red-500" />
            default:
              return <div className="h-5 w-5 rounded-full border-2 border-gray-300" />
          }
        }

        const getStepColor = () => {
          switch (status) {
            case "completed":
              return "text-green-700"
            case "current":
              return "text-blue-700"
            case "error":
              return "text-red-700"
            default:
              return "text-gray-500"
          }
        }

        const getResultColor = () => {
          switch (status) {
            case "completed":
              return "text-green-600"
            case "current":
              return "text-blue-600"
            case "error":
              return "text-red-600"
            default:
              return "text-gray-600"
          }
        }

        return (
          <div key={index} className="relative flex items-start space-x-4">
            {/* Timeline line */}
            {!isLast && <div className="absolute left-2.5 top-8 h-full w-0.5 bg-gray-200" />}

            {/* Icon */}
            <div className="flex-shrink-0 mt-1">{getIcon()}</div>

            {/* Content */}
            <div className="flex-1 min-w-0">
              <div className="bg-white rounded-lg border border-gray-200 p-4 shadow-sm">
                <h4 className={cn("font-semibold text-lg capitalize", getStepColor())}>
                  {item.step.replace(/-/g, " ")}
                </h4>
                <p className={cn("mt-2 text-sm leading-relaxed", getResultColor())}>{item.result}</p>
              </div>
            </div>
          </div>
        )
      })}
    </div>
  )
}
