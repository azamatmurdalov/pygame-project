#################################### IMPORTS ###################################

import unittest

import pygame
from pygame import draw
from pygame.locals import SRCALPHA
from pygame.tests import test_utils


def get_border_values(surface, width, height):
    """Returns a list containing lists with the values of the surface's
    borders.
    """
    border_top = [surface.get_at((x, 0)) for x in range(width)]
    border_left = [surface.get_at((0, y)) for y in range(height)]
    border_right = [
        surface.get_at((width - 1, y)) for y in range(height)]
    border_bottom = [
        surface.get_at((x, height - 1)) for x in range(width)]

    return [border_top, border_left, border_right, border_bottom]


class DrawEllipseTest(unittest.TestCase):
    """
    Class for testing ellipse().
    """
    def test_ellipse(self):
        """|tags: ignore|

        Draws ellipses of differing sizes on surfaces of differing sizes and
        checks to see if the number of sides touching the border of the surface
        is correct.
        """

        left_top = [(0, 0), (1, 0), (0, 1), (1, 1)]
        sizes = [(4, 4), (5, 4), (4, 5), (5, 5)]
        color = (1, 13, 24, 255)

        def same_size(width, height, border_width):
            """Test for ellipses with the same size as the surface."""
            surface = pygame.Surface((width, height))

            draw.ellipse(
                surface, color, (0, 0, width, height), border_width)            

            # For each of the four borders check if it contains the color
            borders = get_border_values(surface, width, height)
            for border in borders:
                self.assertTrue(color in border)

        def not_same_size(width, height, border_width, left, top):
            """Test for ellipses that aren't the same size as the surface."""
            surface = pygame.Surface((width, height))

            draw.ellipse(surface, color, (left, top, width - 1, height - 1),
                         border_width)

            borders = get_border_values(surface, width, height)

            # Check if two sides of the ellipse are touching the border
            sides_touching = [
                color in border for border in borders].count(True)
            self.assertEqual(sides_touching, 2)

        for width, height in sizes:
            for border_width in (0, 1):
                same_size(width, height, border_width)
                for left, top in left_top:
                    not_same_size(width, height, border_width, left, top)


def lines_set_up():
    """Returns the colors and surfaces needed in the tests for draw.line,
    draw.aaline, draw.lines and draw.aalines.
    """
    colors = [
            (0, 0, 0), (255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0),
            (255, 0, 255), (0, 255, 255), (255, 255, 255)]

    sizes = [(49, 49), (50, 50)]
    depths = [16, 32]
    surfaces = []
    for size in sizes:
        for depth in depths:
            # Create each possible surface type
            surface_default = pygame.display.set_mode(size, 0, depth)
            surface_default_SRCALPHA = pygame.Surface(size, SRCALPHA, depth)
            surface_alpha = surface_default.convert_alpha()
            surface_alpha_SRCALPHA = surface_default_SRCALPHA.convert_alpha()

            surfaces.extend([surface_default, surface_alpha,
                             surface_alpha_SRCALPHA, surface_alpha_SRCALPHA])

    return colors, surfaces


class DrawLineTest(unittest.TestCase):
    """Class for testing line(), aaline(), lines() and aalines().
    """

    def test_line_color(self):
        """|tags: ignore|

        Checks if the line drawn with line_is_color() is the correct color.
        """

        def line_is_color(surface, color, draw_line):
            """
            Returns True if draw_line is drawn with the correct color on the
            given surface.
            """
            draw_line(surface, color, (0, 0), (1, 0))
            return surface.get_at((0, 0)) == color

        for draw_line in [draw.line, draw.aaline]:
            colors, surfaces = lines_set_up()
            for surface in surfaces:
                for color in colors:
                    self.assertTrue(line_is_color(surface, color, draw_line))

    def test_line_gaps(self):
        """|tags: ignore|

        Tests if the line drawn with line_has_gaps() contains any gaps.

        See: #512
        """

        def line_has_gaps(surface, draw_line):
            """Returns True if the line drawn on the surface contains gaps.
            """
            width = surface.get_width()
            color = (255, 255, 255)

            draw_line(surface, color, (0, 0), (width - 1, 0))

            colors = [surface.get_at((x, 0)) for x in range(width)]

            return len(colors) == colors.count(color)

        for draw_line in [draw.line, draw.aaline]:
            _, surfaces = lines_set_up()
            for surface in surfaces:
                self.assertTrue(line_has_gaps(surface, draw_line))

    def test_lines_color(self):
        """|tags: ignore|

        Tests if the lines drawn with lines_are_color() are the correct color.
        """
        def lines_are_color(surface, color, draw_lines):
            """Draws (aa)lines around the border of the given surface and
            checks if all borders of the surface only contain the given color.
            """
            width = surface.get_width()
            height = surface.get_height()
            points = [(0, 0), (width - 1, 0), (width - 1, height - 1),
                      (0, height - 1)]

            draw_lines(surface, color, True, points)

            borders = get_border_values(surface, width, height)
            return [all(c == color for c in border) for border in borders]

        for draw_lines in [draw.lines, draw.aalines]:
            colors, surfaces = lines_set_up()
            for surface in surfaces:
                for color in colors:
                    in_border = lines_are_color(surface, color, draw_lines)
                    self.assertTrue(all(in_border))

    def test_lines_gaps(self):
        """|tags: ignore|

        Tests if the lines drawn with lines_have_gaps() contain any gaps.

        See: #512
        """

        def lines_have_gaps(surface, draw_lines):
            """Draws (aa)lines around the border of the given surface and
            checks if all borders of the surface contain any gaps.
            """
            width = surface.get_width()
            height = surface.get_height()
            color = (255, 255, 255)
            points = [(0, 0), (width - 1, 0), (width - 1, height - 1),
                      (0, height - 1)]

            draw_lines(surface, color, True, points)

            borders = get_border_values(surface, width, height)
            return [all(c == color for c in border) for border in borders]

        for draw_lines in [draw.lines, draw.aalines]:
            _, surfaces = lines_set_up()
            for surface in surfaces:
                no_gaps = lines_have_gaps(surface, draw_lines)
                self.assertTrue(all(no_gaps))


class DrawModuleTest(unittest.TestCase):
    def setUp(self):
        (self.surf_w, self.surf_h) = self.surf_size = (320, 200)
        self.surf = pygame.Surface(self.surf_size, pygame.SRCALPHA)
        self.color = (1, 13, 24, 205)

    def test_rect__fill(self):
        # __doc__ (as of 2008-06-25) for pygame.draw.rect:

          # pygame.draw.rect(Surface, color, Rect, width=0): return Rect
          # draw a rectangle shape

        rect = pygame.Rect(10, 10, 25, 20)
        drawn = draw.rect(self.surf, self.color, rect, 0)

        self.assert_(drawn == rect)

        # Should be colored where it's supposed to be
        for pt in test_utils.rect_area_pts(rect):
            color_at_pt = self.surf.get_at(pt)
            self.assert_(color_at_pt == self.color)

        # And not where it shouldn't
        for pt in test_utils.rect_outer_bounds(rect):
            color_at_pt = self.surf.get_at(pt)
            self.assert_(color_at_pt != self.color)

        # Issue #310: Cannot draw rectangles that are 1 pixel high
        bgcolor = pygame.Color('black')
        self.surf.fill(bgcolor)
        hrect = pygame.Rect(1, 1, self.surf_w - 2, 1)
        vrect = pygame.Rect(1, 3, 1, self.surf_h - 4)
        drawn = draw.rect(self.surf, self.color, hrect, 0)
        self.assert_(drawn == hrect)
        x, y = hrect.topleft
        w, h = hrect.size
        self.assertEqual(self.surf.get_at((x - 1, y)), bgcolor)
        self.assertEqual(self.surf.get_at((x + w, y)), bgcolor)
        for i in range(x, x + w):
            self.assertEqual(self.surf.get_at((i, y)), self.color)
        drawn = draw.rect(self.surf, self.color, vrect, 0)
        self.assertEqual(drawn, vrect)
        x, y = vrect.topleft
        w, h = vrect.size
        self.assertEqual(self.surf.get_at((x, y - 1)), bgcolor)
        self.assertEqual(self.surf.get_at((x, y + h)), bgcolor)
        for i in range(y, y + h):
            self.assertEqual(self.surf.get_at((x, i)), self.color)

    def test_rect__one_pixel_lines(self):
        # __doc__ (as of 2008-06-25) for pygame.draw.rect:

          # pygame.draw.rect(Surface, color, Rect, width=0): return Rect
          # draw a rectangle shape
        rect = pygame.Rect(10, 10, 56, 20)

        drawn = draw.rect(self.surf, self.color, rect, 1)
        self.assert_(drawn == rect)

        # Should be colored where it's supposed to be
        for pt in test_utils.rect_perimeter_pts(drawn):
            color_at_pt = self.surf.get_at(pt)
            self.assert_(color_at_pt == self.color)

        # And not where it shouldn't
        for pt in test_utils.rect_outer_bounds(drawn):
            color_at_pt = self.surf.get_at(pt)
            self.assert_(color_at_pt != self.color)

    def test_line(self):

        # __doc__ (as of 2008-06-25) for pygame.draw.line:

          # pygame.draw.line(Surface, color, start_pos, end_pos, width=1): return Rect
          # draw a straight line segment

        # (l, t), (l, t)
        drawn = draw.line(self.surf, self.color, (1, 0), (200, 0))
        self.assert_(drawn.right == 201,
                     "end point arg should be (or at least was) inclusive")

        # Should be colored where it's supposed to be
        for pt in test_utils.rect_area_pts(drawn):
            self.assert_(self.surf.get_at(pt) == self.color)

        # And not where it shouldn't
        for pt in test_utils.rect_outer_bounds(drawn):
            self.assert_(self.surf.get_at(pt) != self.color)

        # Line width greater that 1
        line_width = 2
        offset = 5
        a = (offset, offset)
        b = (self.surf_size[0] - offset, a[1])
        c = (a[0], self.surf_size[1] - offset)
        d = (b[0], c[1])
        e = (a[0] + offset, c[1])
        f = (b[0], c[0] + 5)
        lines = [(a, d), (b, c), (c, b), (d, a),
                 (a, b), (b, a), (a, c), (c, a),
                 (a, e), (e, a), (a, f), (f, a),
                 (a, a),]
        for p1, p2 in lines:
            msg = "%s - %s" % (p1, p2)
            if p1[0] <= p2[0]:
                plow = p1
                phigh = p2
            else:
                plow = p2
                phigh = p1
            self.surf.fill((0, 0, 0))
            rec = draw.line(self.surf, (255, 255, 255), p1, p2, line_width)
            xinc = yinc = 0
            if abs(p1[0] - p2[0]) > abs(p1[1] - p2[1]):
                yinc = 1
            else:
                xinc = 1
            for i in range(line_width):
                p = (p1[0] + xinc * i, p1[1] + yinc * i)
                self.assert_(self.surf.get_at(p) == (255, 255, 255), msg)
                p = (p2[0] + xinc * i, p2[1] + yinc * i)
                self.assert_(self.surf.get_at(p) == (255, 255, 255), msg)
            p = (plow[0] - 1, plow[1])
            self.assert_(self.surf.get_at(p) == (0, 0, 0), msg)
            p = (plow[0] + xinc * line_width, plow[1] + yinc * line_width)
            self.assert_(self.surf.get_at(p) == (0, 0, 0), msg)
            p = (phigh[0] + xinc * line_width, phigh[1] + yinc * line_width)
            self.assert_(self.surf.get_at(p) == (0, 0, 0), msg)
            if p1[0] < p2[0]:
                rx = p1[0]
            else:
                rx = p2[0]
            if p1[1] < p2[1]:
                ry = p1[1]
            else:
                ry = p2[1]
            w = abs(p2[0] - p1[0]) + 1 + xinc * (line_width - 1)
            h = abs(p2[1] - p1[1]) + 1 + yinc * (line_width - 1)
            msg += ", %s" % (rec,)
            self.assert_(rec == (rx, ry, w, h), msg)

    def todo_test_arc(self):

        # __doc__ (as of 2008-08-02) for pygame.draw.arc:

          # pygame.draw.arc(Surface, color, Rect, start_angle, stop_angle,
          # width=1): return Rect
          #
          # draw a partial section of an ellipse
          #
          # Draws an elliptical arc on the Surface. The rect argument is the
          # area that the ellipse will fill. The two angle arguments are the
          # initial and final angle in radians, with the zero on the right. The
          # width argument is the thickness to draw the outer edge.
          #

        self.fail()

    def todo_test_circle(self):

        # __doc__ (as of 2008-08-02) for pygame.draw.circle:

          # pygame.draw.circle(Surface, color, pos, radius, width=0): return Rect
          # draw a circle around a point
          #
          # Draws a circular shape on the Surface. The pos argument is the
          # center of the circle, and radius is the size. The width argument is
          # the thickness to draw the outer edge. If width is zero then the
          # circle will be filled.
          #

        self.fail()


RED = pygame.Color('red')
GREEN = pygame.Color('green')

SQUARE = ([0, 0], [3, 0], [3, 3], [0, 3])
DIAMOND = [(1, 3), (3, 5), (5, 3), (3, 1)]
CROSS = ([2, 0], [4, 0], [4, 2], [6, 2],
         [6, 4], [4, 4], [4, 6], [2, 6],
         [2, 4], [0, 4], [0, 2], [2, 2])


class DrawPolygonTest(unittest.TestCase):

    def setUp(self):
        self.surface = pygame.Surface((20, 20))

    def test_draw_square(self):
        pygame.draw.polygon(self.surface, RED, SQUARE, 0)
        # note : there is a discussion (#234) if draw.polygon should include or
        # not the right or lower border; here we stick with current behavior,
        # eg include those borders ...
        for x in range(4):
            for y in range(4):
                self.assertEqual(self.surface.get_at((x, y)), RED)

    def test_draw_diamond(self):
        pygame.draw.rect(self.surface, RED, (0, 0, 10, 10), 0)
        pygame.draw.polygon(self.surface, GREEN, DIAMOND, 0)
        # this diamond shape is equivalent to its four corners, plus inner square
        for x, y in DIAMOND:
            self.assertEqual(self.surface.get_at((x, y)), GREEN, msg=str((x, y)))
        for x in range(2, 5):
            for y in range(2, 5):
                self.assertEqual(self.surface.get_at((x, y)), GREEN)

    def test_1_pixel_high_or_wide_shapes(self):
        # 1. one-pixel-high, filled
        pygame.draw.rect(self.surface, RED, (0, 0, 10, 10), 0)
        pygame.draw.polygon(self.surface, GREEN, [(x, 2) for x, y in CROSS], 0)
        cross_size = 6 # the maxium x or y coordinate of the cross
        for x in range(cross_size + 1):
            self.assertEqual(self.surface.get_at((x, 1)), RED)
            self.assertEqual(self.surface.get_at((x, 2)), GREEN)
            self.assertEqual(self.surface.get_at((x, 3)), RED)
        pygame.draw.rect(self.surface, RED, (0, 0, 10, 10), 0)
        # 2. one-pixel-high, not filled
        pygame.draw.polygon(self.surface, GREEN, [(x, 5) for x, y in CROSS], 1)
        for x in range(cross_size + 1):
            self.assertEqual(self.surface.get_at((x, 4)), RED)
            self.assertEqual(self.surface.get_at((x, 5)), GREEN)
            self.assertEqual(self.surface.get_at((x, 6)), RED)
        pygame.draw.rect(self.surface, RED, (0, 0, 10, 10), 0)
        # 3. one-pixel-wide, filled
        pygame.draw.polygon(self.surface, GREEN, [(3, y) for x, y in CROSS], 0)
        for y in range(cross_size + 1):
            self.assertEqual(self.surface.get_at((2, y)), RED)
            self.assertEqual(self.surface.get_at((3, y)), GREEN)
            self.assertEqual(self.surface.get_at((4, y)), RED)
        pygame.draw.rect(self.surface, RED, (0, 0, 10, 10), 0)
        # 4. one-pixel-wide, not filled
        pygame.draw.polygon(self.surface, GREEN, [(4, y) for x, y in CROSS], 1)
        for y in range(cross_size + 1):
            self.assertEqual(self.surface.get_at((3, y)), RED)
            self.assertEqual(self.surface.get_at((4, y)), GREEN)
            self.assertEqual(self.surface.get_at((5, y)), RED)

    def test_draw_symetric_cross(self):
        '''nonregression on issue #234 : x and y where handled inconsistently.

        Also, the result is/was different wether we fill or not the polygon.
        '''

        # 1. case width = 1 (not filled: `polygon` calls  internally the `lines` function)
        pygame.draw.rect(self.surface, RED, (0, 0, 10, 10), 0)
        pygame.draw.polygon(self.surface, GREEN, CROSS, 1)
        inside = [(x, 3) for x in range(1, 6)] + [(3, y) for y in range(1, 6)]
        for x in range(10):
            for y in range(10):
                if (x, y) in inside:
                    self.assertEqual(self.surface.get_at((x, y)), RED)
                elif (x in range(2, 5) and y <7) or (y in range(2, 5) and x < 7):
                    # we are on the border of the cross:
                    self.assertEqual(self.surface.get_at((x, y)), GREEN)
                else:
                    # we are outside
                    self.assertEqual(self.surface.get_at((x, y)), RED)

        # 2. case width = 0 (filled; this is the example from #234)
        pygame.draw.rect(self.surface, RED, (0, 0, 10, 10), 0)
        pygame.draw.polygon(self.surface, GREEN, CROSS, 0)
        inside = [(x, 3) for x in range(1, 6)] + [(3, y) for y in range(1, 6)]
        for x in range(10):
            for y in range(10):
                if (x in range(2, 5) and y <7) or (y in range(2, 5) and x < 7):
                    # we are on the border of the cross:
                    self.assertEqual(self.surface.get_at((x, y)), GREEN, msg=str((x, y)))
                else:
                    # we are outside
                    self.assertEqual(self.surface.get_at((x, y)), RED)

    def test_illumine_shape(self):
        '''non regression on issue #313 '''
        rect = pygame.Rect((0, 0, 20, 20))
        path_data = [(0, 0), (rect.width-1, 0), # upper border
                     (rect.width-5,  5-1), (5-1, 5-1),  # upper inner
                     (5- 1, rect.height-5), (0,  rect.height-1)]   # lower diagonal
        # The shape looks like this (the numbers are the indices of path_data)

        # 0**********************1              <-- upper border
        # ***********************
        # **********************
        # *********************
        # ****3**************2                  <-- upper inner border
        # *****
        # *****                   (more lines here)
        # *****
        # ****4
        # ****
        # ***
        # **
        # 5
        #

        # the current bug is that the "upper inner" line is not drawn, but only
        # if 4 or some lower corner exists
        pygame.draw.rect(self.surface, RED, (0, 0, 20, 20), 0)

        # 1. First without the corners 4 & 5
        pygame.draw.polygon(self.surface, GREEN, path_data[:4], 0)
        for x in range(20):
            self.assertEqual(self.surface.get_at((x, 0)), GREEN)  # upper border
        for x in range(4, rect.width-5 +1):
            self.assertEqual(self.surface.get_at((x, 4)), GREEN)  # upper inner

        # 2. with the corners 4 & 5
        pygame.draw.rect(self.surface, RED, (0, 0, 20, 20), 0)
        pygame.draw.polygon(self.surface, GREEN, path_data, 0)
        for x in range(4, rect.width-5 +1):
            self.assertEqual(self.surface.get_at((x, 4)), GREEN)  # upper inner



################################################################################

if __name__ == '__main__':
    unittest.main()
