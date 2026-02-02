# Path: scaffold/symphony/polyglot/wards/ruby_ward.py

def get_harness(sanctum_abs_path: str) -> str:
    """Returns the Gnostic Ward Harness for the Ruby runtime."""
    return f'''
# --- BEGIN SCAFFOLD GNOSTIC WARD (RUBY) ---
require 'pathname'

$__sc_sanctum_path__ = Pathname.new('{sanctum_abs_path}').realpath
puts "--- Gnostic Filesystem Ward Engaged (Sanctum: #{{$__sc_sanctum_path__}}) ---"

def __sc_path_adjudicator__(path_str, rite_name)
  begin
    abs_path = Pathname.new(path_str).realpath
    unless abs_path.to_s.start_with?($__sc_sanctum_path__.to_s)
      raise PermissionError, "[Gnostic Ward Heresy] The '#{{rite_name}}' rite\\'s attempt to access '#{{abs_path}}' outside the sacred sanctum was struck down."
    end
  rescue => e
    raise PermissionError, "[Gnostic Ward Heresy] A paradox occurred while adjudicating '#{{path_str}}': #{{e.message}}"
  end
end

class File
  # Save the profane, original rite
  class << self
    alias_method :__sc_profane_open__, :open
  end

  # Forge the new, Gnostically-aware rite
  def self.open(*args, &block)
    __sc_path_adjudicator__(args[0], 'File.open')
    __sc_profane_open__(*args, &block)
  end
end

class Pathname
  # Save the profane, original rite
  alias_method :__sc_profane_initialize__, :initialize

  # Forge the new, Gnostically-aware rite
  def initialize(path)
    # The Gaze is upon the very moment of a Pathname's birth.
    __sc_path_adjudicator__(path, 'Pathname.new')
    __sc_profane_initialize__(path)
  end
end
# --- END SCAFFOLD GNOSTIC WARD ---
'''

