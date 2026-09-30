import { useState, useEffect } from 'react'
import { LogOut, Plus, FileText, Download } from 'lucide-react'

interface Template {
  id: string
  name: string
  content: string
}

interface Dashboard {
  token: string
  onLogout: () => void
}

export function Dashboard({ token, onLogout }: Dashboard) {
  const [templates, setTemplates] = useState<Template[]>([])
  const [loading, setLoading] = useState(false)
  const [selectedTemplate, setSelectedTemplate] = useState<Template | null>(null)
  const [fields, setFields] = useState<Record<string, string>>({})

  const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'

  useEffect(() => {
    fetchTemplates()
  }, [])

  const fetchTemplates = async () => {
    setLoading(true)
    try {
      const response = await fetch(`${apiUrl}/api/templates`, {
        headers: { 'Authorization': `Bearer ${token}` },
      })
      if (response.ok) {
        const data = await response.json()
        setTemplates(data)
      }
    } catch (err) {
      console.error('Failed to fetch templates:', err)
    } finally {
      setLoading(false)
    }
  }

  const handleTemplateSelect = (template: Template) => {
    setSelectedTemplate(template)
    const fieldMatches = template.content.match(/\{([a-zA-Z_][a-zA-Z0-9_]*)\}/g)
    const fieldNames = fieldMatches ? fieldMatches.map(f => f.slice(1, -1)) : []
    const newFields: Record<string, string> = {}
    fieldNames.forEach(name => {
      newFields[name] = ''
    })
    setFields(newFields)
  }

  const handleFieldChange = (field: string, value: string) => {
    setFields({ ...fields, [field]: value })
  }

  const handleExport = async (format: string) => {
    if (!selectedTemplate) return
    try {
      const response = await fetch(
        `${apiUrl}/api/documents/export`,
        {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            template_id: selectedTemplate.id,
            fields,
            format,
          }),
        }
      )
      if (response.ok) {
        const blob = await response.blob()
        const url = window.URL.createObjectURL(blob)
        const a = document.createElement('a')
        a.href = url
        a.download = `document.${format.toLowerCase()}`
        a.click()
      }
    } catch (err) {
      console.error('Export failed:', err)
    }
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 py-4 flex justify-between items-center">
          <h1 className="text-xl font-bold text-gray-900">MP Electric - Document Automation</h1>
          <button
            onClick={onLogout}
            className="flex items-center gap-2 px-4 py-2 text-gray-700 hover:bg-gray-100 rounded-lg"
          >
            <LogOut size={18} />
            Logout
          </button>
        </div>
      </nav>

      <div className="max-w-7xl mx-auto px-4 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          <div>
            <h2 className="text-lg font-semibold text-gray-900 mb-4">Templates</h2>
            {loading ? (
              <p className="text-gray-600">Loading...</p>
            ) : (
              <div className="space-y-2">
                {templates.map((template) => (
                  <button
                    key={template.id}
                    onClick={() => handleTemplateSelect(template)}
                    className={`w-full p-4 rounded-lg border-2 text-left transition ${
                      selectedTemplate?.id === template.id
                        ? 'border-blue-500 bg-blue-50'
                        : 'border-gray-200 bg-white hover:border-gray-300'
                    }`}
                  >
                    <div className="flex items-center gap-2">
                      <FileText size={18} />
                      <span className="font-medium">{template.name}</span>
                    </div>
                  </button>
                ))}
              </div>
            )}
          </div>

          {selectedTemplate && (
            <div className="lg:col-span-2">
              <h2 className="text-lg font-semibold text-gray-900 mb-4">{selectedTemplate.name}</h2>
              <div className="bg-white p-6 rounded-lg shadow-sm space-y-4">
                {Object.keys(fields).map((field) => (
                  <div key={field}>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      {field}
                    </label>
                    <input
                      type="text"
                      value={fields[field]}
                      onChange={(e) => handleFieldChange(field, e.target.value)}
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
                  </div>
                ))}

                <div className="pt-4 border-t">
                  <p className="text-sm text-gray-600 mb-4">Export as:</p>
                  <div className="grid grid-cols-2 gap-2">
                    {['PDF', 'DOCX', 'XLSX', 'PPTX', 'CSV'].map((format) => (
                      <button
                        key={format}
                        onClick={() => handleExport(format)}
                        className="flex items-center justify-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 text-sm font-medium"
                      >
                        <Download size={16} />
                        {format}
                      </button>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
