"""
animations.py - Cinematic animations and effects
"""

from PySide6.QtCore import QPropertyAnimation, QEasingCurve, QParallelAnimationGroup
from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QColor


class AnimationManager:
    """Manages cinematic animations for UI elements"""
    
    @staticmethod
    def fade_in(widget: QWidget, duration: int = 500):
        """Fade in animation"""
        animation = QPropertyAnimation(widget, b"windowOpacity")
        animation.setDuration(duration)
        animation.setStartValue(0)
        animation.setEndValue(1)
        animation.setEasingCurve(QEasingCurve.InOutCubic)
        return animation
    
    @staticmethod
    def fade_out(widget: QWidget, duration: int = 500):
        """Fade out animation"""
        animation = QPropertyAnimation(widget, b"windowOpacity")
        animation.setDuration(duration)
        animation.setStartValue(1)
        animation.setEndValue(0)
        animation.setEasingCurve(QEasingCurve.InOutCubic)
        return animation
    
    @staticmethod
    def slide_in(widget: QWidget, direction: str = 'left', duration: int = 400):
        """Slide in from direction"""
        animation = QPropertyAnimation(widget, b"pos")
        animation.setDuration(duration)
        animation.setEasingCurve(QEasingCurve.OutBack)
        
        start_pos = widget.pos()
        if direction == 'left':
            animation.setStartValue(start_pos - widget.rect().topRight())
        elif direction == 'right':
            animation.setStartValue(start_pos + widget.rect().topRight())
        elif direction == 'top':
            animation.setStartValue(start_pos - widget.rect().bottomLeft())
        elif direction == 'bottom':
            animation.setStartValue(start_pos + widget.rect().bottomLeft())
        
        animation.setEndValue(start_pos)
        return animation
    
    @staticmethod
    def pulse(widget: QWidget, duration: int = 1000):
        """Pulse animation (scale)"""
        animation = QPropertyAnimation(widget, b"geometry")
        animation.setDuration(duration)
        animation.setLoopCount(-1)  # Infinite
        
        start_geo = widget.geometry()
        animation.setKeyValueAt(0, start_geo)
        animation.setKeyValueAt(0.5, start_geo.adjusted(-5, -5, 5, 5))
        animation.setKeyValueAt(1, start_geo)
        animation.setEasingCurve(QEasingCurve.InOutSine)
        return animation
    
    @staticmethod
    def color_cycle(widget: QWidget, colors: list, duration: int = 3000):
        """Cycle through colors"""
        animation = QPropertyAnimation(widget, b"styleSheet")
        animation.setDuration(duration)
        animation.setLoopCount(-1)
        
        keyframes = []
        step = 1.0 / len(colors)
        for i, color in enumerate(colors):
            keyframes.append((i * step, f"background-color: {color};"))
        
        for keyframe, style in keyframes:
            animation.setKeyValueAt(keyframe, style)
        
        return animation
    
    @staticmethod
    def purchase_animation(widget: QWidget):
        """Special animation for product purchase"""
        group = QParallelAnimationGroup()
        
        # Scale up
        scale = QPropertyAnimation(widget, b"geometry")
        scale.setDuration(300)
        start_geo = widget.geometry()
        scale.setStartValue(start_geo)
        scale.setKeyValueAt(0.5, start_geo.adjusted(-10, -10, 10, 10))
        scale.setEndValue(start_geo)
        scale.setEasingCurve(QEasingCurve.OutBack)
        
        # Color flash
        color = QPropertyAnimation(widget, b"styleSheet")
        color.setDuration(300)
        original_style = widget.styleSheet()
        color.setStartValue(original_style)
        color.setKeyValueAt(0.5, original_style + "background-color: #00ff88;")
        color.setEndValue(original_style)
        
        group.addAnimation(scale)
        group.addAnimation(color)
        return group
    
    @staticmethod
    def money_insert_animation(widget: QWidget):
        """Animation for money insertion"""
        group = QParallelAnimationGroup()
        
        # Shake animation
        shake = QPropertyAnimation(widget, b"pos")
        shake.setDuration(200)
        start_pos = widget.pos()
        shake.setKeyValueAt(0, start_pos)
        shake.setKeyValueAt(0.25, start_pos + widget.rect().topRight() * 0.1)
        shake.setKeyValueAt(0.5, start_pos - widget.rect().topRight() * 0.1)
        shake.setKeyValueAt(0.75, start_pos + widget.rect().topRight() * 0.1)
        shake.setEndValue(start_pos)
        
        # Glow effect
        glow = QPropertyAnimation(widget, b"styleSheet")
        glow.setDuration(200)
        original_style = widget.styleSheet()
        glow.setStartValue(original_style)
        glow.setKeyValueAt(0.5, original_style + "box-shadow: 0 0 20px gold;")
        glow.setEndValue(original_style)
        
        group.addAnimation(shake)
        group.addAnimation(glow)
        return group


class ParticleEffect:
    """Creates particle effects for special events"""
    
    @staticmethod
    def create_confetti(parent: QWidget, count: int = 50):
        """Create falling confetti effect"""
        particles = []
        for _ in range(count):
            particle = QLabel("✨", parent)
            particle.setStyleSheet("font-size: 20px; color: gold;")
            particle.show()
            particles.append(particle)
        return particles
    
    @staticmethod
    def animate_confetti(particles: list, duration: int = 2000):
        """Animate confetti falling"""
        animations = []
        for particle in particles:
            anim = QPropertyAnimation(particle, b"pos")
            anim.setDuration(duration)
            start_x = particle.pos().x()
            start_y = -20
            anim.setStartValue(particle.parent().mapFromGlobal(particle.pos()))
            anim.setEndValue(particle.parent().mapFromGlobal(
                particle.pos() + particle.rect().bottomLeft() * 3
            ))
            anim.setEasingCurve(QEasingCurve.InQuad)
            animations.append(anim)
        return animations
