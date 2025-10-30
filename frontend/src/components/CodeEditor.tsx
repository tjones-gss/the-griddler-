interface CodeEditorProps {
  value: string
  onChange: (value: string) => void
  placeholder?: string
  readOnly?: boolean
  height?: string
}

export default function CodeEditor({
  value,
  onChange,
  placeholder = 'Enter code here...',
  readOnly = false,
  height = '300px'
}: CodeEditorProps) {
  return (
    <textarea
      value={value}
      onChange={(e) => onChange(e.target.value)}
      placeholder={placeholder}
      readOnly={readOnly}
      className={`
        w-full p-4 border border-gray-300 rounded-lg
        font-mono text-sm
        focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent
        resize-none
        ${readOnly ? 'bg-gray-50 cursor-not-allowed' : 'bg-white'}
      `}
      style={{ height }}
    />
  )
}
