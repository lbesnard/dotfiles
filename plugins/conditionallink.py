import os
import sys
import re
import dotbot
import dotbot.util


class ConditionalLink(dotbot.Plugin):
    """
    Conditionally links desktop files only if their referenced AppImage exists.
    Parses the Exec= line from desktop files to determine the AppImage path.
    """

    _directive = "conditionallink"

    def can_handle(self, directive):
        return directive == self._directive

    def handle(self, directive, data):
        if directive != self._directive:
            raise ValueError("ConditionalLink cannot handle directive %s" % directive)
        return self._process_conditional_links(data)

    def _process_conditional_links(self, links):
        """
        Process conditional links.
        
        Config format:
        - conditionallink:
            ~/.local/share/applications/app.desktop:
              path: desktop/app.desktop
        """
        success = True
        defaults = self._context.defaults().get("conditionallink", {})
        
        for destination, source in links.items():
            destination = os.path.expandvars(destination)
            relative = defaults.get("relative", False)
            canonical_path = defaults.get("canonicalize", defaults.get("canonicalize-path", True))
            force = defaults.get("force", False)
            create = defaults.get("create", False)
            
            if isinstance(source, dict):
                # extended config
                relative = source.get("relative", relative)
                canonical_path = source.get("canonicalize", source.get("canonicalize-path", canonical_path))
                force = source.get("force", force)
                create = source.get("create", create)
                source_path = source.get("path", source.get("path"))
            else:
                source_path = source
            
            if source_path is None:
                self._log.error("ConditionalLink: no path specified for %s" % destination)
                success = False
                continue
            
            # Expand and make relative to dotfiles directory
            if not os.path.isabs(source_path):
                source_path = os.path.join(self._context.base_directory(), source_path)
            
            source_path = os.path.expandvars(source_path)
            
            # Check if source (desktop file) exists
            if not os.path.exists(source_path):
                self._log.error("ConditionalLink: source file does not exist: %s" % source_path)
                success = False
                continue
            
            # Extract AppImage path from desktop file
            appimage_path = self._extract_appimage_path(source_path)
            
            if appimage_path is None:
                self._log.warning("ConditionalLink: could not extract Exec path from %s" % source_path)
                success = False
                continue
            
            # Expand variables (e.g., $HOME)
            appimage_path = os.path.expandvars(appimage_path)
            appimage_path = os.path.expanduser(appimage_path)
            
            # Check if AppImage exists
            if not os.path.exists(appimage_path):
                self._log.warning("ConditionalLink: AppImage not found, skipping link: %s (expected: %s)" % (destination, appimage_path))
                continue
            
            # Now create the symlink (reuse logic from dotbot's link plugin)
            if self._create_link(destination, source_path, relative, force, create, canonical_path):
                self._log.info("ConditionalLink: linked %s" % destination)
            else:
                success = False
        
        return success
    
    def _extract_appimage_path(self, desktop_file_path):
        """
        Parse a .desktop file and extract the Exec= line.
        Returns the first word of the Exec line (the actual executable path).
        """
        try:
            with open(desktop_file_path, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line.startswith('Exec='):
                        # Extract the command from Exec=
                        exec_line = line[5:]  # Remove 'Exec='
                        # Split by spaces and take the first token (the executable)
                        # Handle potential trailing arguments/flags
                        executable = exec_line.split()[0]
                        return executable
        except Exception as e:
            self._log.error("ConditionalLink: error reading desktop file %s: %s" % (desktop_file_path, str(e)))
        
        return None
    
    def _create_link(self, destination, source, relative, force, create, canonical_path):
        """
        Create a symlink from destination to source.
        Simplified version of dotbot's link logic.
        """
        try:
            # Create parent directory if needed
            if create:
                parent_dir = os.path.dirname(destination)
                if not os.path.exists(parent_dir):
                    os.makedirs(parent_dir)
            
            # Determine the target for the symlink
            if relative:
                # Make path relative
                destination_dir = os.path.dirname(os.path.abspath(destination))
                if canonical_path:
                    source = os.path.realpath(source)
                target = os.path.relpath(source, destination_dir)
            else:
                if canonical_path:
                    target = os.path.realpath(source)
                else:
                    target = os.path.abspath(source)
            
            # Remove existing link if force is True
            if os.path.lexists(destination):
                if force:
                    os.remove(destination)
                else:
                    # Link already exists
                    if os.path.islink(destination) and os.readlink(destination) == target:
                        self._log.debug("ConditionalLink: link already correct for %s" % destination)
                        return True
                    else:
                        self._log.error("ConditionalLink: destination already exists: %s" % destination)
                        return False
            
            # Create the symlink
            os.symlink(target, destination)
            return True
        
        except Exception as e:
            self._log.error("ConditionalLink: error creating link %s -> %s: %s" % (destination, source, str(e)))
            return False
