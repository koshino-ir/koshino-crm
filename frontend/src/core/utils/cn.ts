import { type ClassValue, clsx } from "clsx"
import { twMerge } from "tailwind-merge"

/**
 * Merge Tailwind classes with proper conflict resolution.
 * Usage: cn("px-2 py-1", props.class)
 */
export function cn(...inputs: ClassValue[]): string {
    return twMerge(clsx(inputs))
}