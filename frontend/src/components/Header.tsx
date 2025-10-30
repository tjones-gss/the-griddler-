import { Code2, Grid3x3 } from 'lucide-react'

export default function Header() {
  return (
    <header className="bg-gradient-to-r from-blue-600 to-blue-700 text-white shadow-lg">
      <div className="container mx-auto px-4 py-6">
        <div className="flex items-center gap-3">
          <div className="relative">
            <Grid3x3 className="w-10 h-10" />
            <Code2 className="w-5 h-5 absolute -bottom-1 -right-1 bg-blue-500 rounded-full p-0.5" />
          </div>
          <div>
            <h1 className="text-3xl font-bold tracking-tight">The Griddler</h1>
            <p className="text-blue-100 text-sm">COBOL REPEAT GROUP → SCR100 Parser</p>
          </div>
        </div>
      </div>
    </header>
  )
}
