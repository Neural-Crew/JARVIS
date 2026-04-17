import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

/**
 * Fusionne des classes CSS avec tailwind-merge et clsx.
 * @param {...ClassValue[]} inputs - Les classes ou conditions de classes à fusionner.
 * @returns {string} La chaîne de classes fusionnée et optimisée pour Tailwind.
 */
export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}
