import React from 'react'
import { cn, getInitials } from '@/lib/utils'

export interface AvatarProps extends React.HTMLAttributes<HTMLDivElement> {
  src?: string
  alt?: string
  name?: string
  size?: 'sm' | 'md' | 'lg' | 'xl'
  fallback?: string
}

const Avatar = React.forwardRef<HTMLDivElement, AvatarProps>(
  ({ className, src, alt, name, size = 'md', fallback, ...props }, ref) => {
    const [imageError, setImageError] = React.useState(false)

    const sizes = {
      sm: 'h-8 w-8 text-xs',
      md: 'h-10 w-10 text-sm',
      lg: 'h-12 w-12 text-base',
      xl: 'h-16 w-16 text-lg',
    }

    const displayInitials = fallback || getInitials(name || alt || '')

    if (src && !imageError) {
      return (
        <div
          ref={ref}
          className={cn(
            'relative shrink-0 overflow-hidden rounded-full bg-slate-200 dark:bg-slate-700',
            sizes[size],
            className
          )}
          {...props}
        >
          <img
            src={src}
            alt={alt}
            className="aspect-square h-full w-full object-cover"
            onError={() => setImageError(true)}
          />
        </div>
      )
    }

    // Generate a consistent color based on name
    const getAvatarColor = (name: string) => {
      const colors = [
        'bg-primary-500',
        'bg-success-500',
        'bg-warning-500',
        'bg-error-500',
        'bg-purple-500',
        'bg-pink-500',
        'bg-indigo-500',
        'bg-teal-500',
      ]
      let hash = 0
      for (let i = 0; i < name.length; i++) {
        hash = name.charCodeAt(i) + ((hash << 5) - hash)
      }
      return colors[Math.abs(hash) % colors.length]
    }

    return (
      <div
        ref={ref}
        className={cn(
          'relative flex shrink-0 items-center justify-center rounded-full font-medium text-white',
          getAvatarColor(name || alt || 'user'),
          sizes[size],
          className
        )}
        {...props}
      >
        {displayInitials}
      </div>
    )
  }
)

Avatar.displayName = 'Avatar'

export { Avatar }
